import shutil
from pathlib import Path

from enum import StrEnum
from typing import Any, cast

from anthropic import Anthropic
from anthropic.types import (
    ImageBlockParam,
    Message,
    MessageParam,
    TextBlock,
    TextBlockParam,
    ToolResultBlockParam,
    ToolUseBlockParam,
)

from config.prompt import SYSTEM_PROMPT
from tools.collection import ToolCollection, ToolResult
from tools.browser import BrowserTool
from tools.script_writer import ScriptWriterTool

class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"

PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-sonnet-4-5-20250929",
    # APIProvider.BEDROCK: "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
}

PROVIDER = APIProvider.ANTHROPIC
MODEL = PROVIDER_TO_DEFAULT_MODEL_NAME[PROVIDER]

async def test_gen_loop(
        website_url: str,
        test_case: str,
        max_tokens: int = 4096
) -> list[MessageParam]:
    """
    The agent loop that executes the interaction between AI and tool
    """
    messages: list[MessageParam] = [{"role": "user", "content": test_case}]

    _clear_screenshots()

    # Create the tools
    browser_tool = BrowserTool(website_url)
    await browser_tool.start()  # Start it (returns None)

    script_writer = ScriptWriterTool()

    tool_collection = ToolCollection(browser_tool, script_writer)
    system_prompt = TextBlockParam(type="text", text=SYSTEM_PROMPT)
    client = Anthropic(
        api_key=""
    )

    try:
        
        while True:
            try:
                raw_response = client.messages.with_raw_response.create(
                    max_tokens=max_tokens,
                    messages=messages,
                    model=MODEL,
                    system=[system_prompt],
                    tools=tool_collection.to_params(),
                )
            except Exception as e:
                print(f"API call failed: {e}")
                return messages

            response = raw_response.parse()
            print("******* New instructions received *******\n")
            response_params = _response_to_params(response)
            messages.append({"role": "assistant", "content": response_params})

            tool_result_content, final_agent_message = await _process_tool_use(tool_collection, response_params)
            if not tool_result_content:
                return final_agent_message

            messages.append({"content": tool_result_content, "role": "user"})
    finally:
        print("Closing browser...")
        await browser_tool.close()
        print("Browser closed")

    
def _response_to_params(
        response: Message
) -> list[TextBlockParam | ToolUseBlockParam]:
    
    return [
        {"type": "text", "text": block.text} if isinstance(block, TextBlock)
        else cast(ToolUseBlockParam, block.model_dump())
        for block in response.content
    ]


async def _process_tool_use(
        tool_collection: ToolCollection,
        response_params: list[TextBlockParam | ToolUseBlockParam]
) -> list[ToolResultBlockParam]:
    tool_result_content = []
    final_agent_message = ''
    for block in response_params:
        print(f'{block}\n')
        if block["type"] == "tool_use":
            result = await tool_collection.run(
                name=block["name"],
                tool_input=cast(dict[str, Any], block["input"]),
            )
            tool_result_content.append(_make_api_tool_result(result, block["id"]))

    if not tool_result_content:
        final_agent_message = response_params[0]['text']
    return tool_result_content, final_agent_message

def _make_api_tool_result(
    result: ToolResult, tool_use_id: str
) -> ToolResultBlockParam:
    """
    Convert a ToolResult to a BetaToolResultBlockParam for the API.
    """
    tool_result_content: list[TextBlockParam | ImageBlockParam] | str = []
    is_error = False

    if result.error:
        is_error = True
        tool_result_content = _maybe_prepend_system_tool_result(result, result.error)
    else:
        if result.output:
            tool_result_content.append({
                "type": "text",
                "text": _maybe_prepend_system_tool_result(result, result.output),
            })
        if result.base64_image:
            tool_result_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": result.base64_image,
                }
            })
    return {
        "type": "tool_result",
        "content": tool_result_content,
        "tool_use_id": tool_use_id,
        "is_error": is_error,
    }

def _maybe_prepend_system_tool_result(result: ToolResult, result_text: str) -> str:
    """
    Prepend system information to the result if available.
    """
    if result.system:
        return f"<system>{result.system}</system>\n{result_text}"
    return result_text

def _clear_screenshots():
    screenshot_dir = Path("../screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove all .png files
    png_files = list(screenshot_dir.glob("*.png"))
    for png_file in png_files:
        png_file.unlink()