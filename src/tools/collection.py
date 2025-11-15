from typing import Any, Dict, List
from anthropic.types import ToolUnionParam
from .base import BaseAnthropicTool, ToolError, ToolFailure, ToolResult


class ToolCollection:

    def __init__(self, *tools: BaseAnthropicTool):

        self.tools = tools

        self.tool_map = {tool.to_params()["name"]: tool for tool in tools}
        
        if len(self.tool_map) != len(tools):
            raise ValueError("Duplicate tool names found in the provided tools.")

    def to_params(self) -> List[ToolUnionParam]:
        return [tool.to_params() for tool in self.tools]

    async def run(self, *, name: str, tool_input: Dict[str, Any]) -> ToolResult:

        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool '{name}' is invalid")

        try:
            # Execute the tool asynchronously
            return await tool(**tool_input)
        except ToolError as e:
            # Handle known tool errors
            return ToolFailure(error=e.message)
        except Exception as e:
            # Handle unexpected exceptions
            return ToolFailure(error=f"Unexpected error: {e}")