from enum import StrEnum
from typing import Any, cast

from anthropic import AnthropicBedrock
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
from tools.collection import ToolCollection

class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"

PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-4-5-sonnet-20250929",
    APIProvider.BEDROCK: "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
}

PROVIDER = APIProvider.BEDROCK
MODEL = PROVIDER_TO_DEFAULT_MODEL_NAME[PROVIDER]

async def test_gen_loop(
        website_url: str,
        test_case: str,
        max_tokens: int = 4096
) -> list[MessageParam]:
    """
    The agent loop that executes the interaction between AI and tool
    """

    messsages: list[MessageParam] = [{"role": "user", "content": test_case}]
    tool_collection = ToolCollection()
    system_prompt = TextBlockParam(type="text", text=SYSTEM_PROMPT)
    client = AnthropicBedrock()

    while True:
        try:
            response = client.messages.create(
                max_tokens=max_tokens,
                messages=messsages,
                model=MODEL,
                system=[system_prompt],
                tools=tool_collection.to_params()
            )
        except Exception as e:
            print(f"API call failed: {e}")
            return messsages
        
        print(response)