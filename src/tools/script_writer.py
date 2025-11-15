from .base import BaseAnthropicTool, ToolResult
from pathlib import Path
from typing import Literal

class ScriptWriterTool(BaseAnthropicTool):
    "Allows for agent to write script files"

    name: Literal["script_writer"] = "script_writer"

    def __init__(self, output_dir: str = "../scripts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def __call__(self, **kwargs) -> ToolResult:
        """Write content to a file"""
        action = kwargs.get("action")
        path = kwargs.get("path")
        content = kwargs.get("content")
        
        try:
            if action == "write":
                if not path or not content:
                    return ToolResult(error="Both 'path' and 'content' are required for write action")
                
                # If path is relative, put it in output_dir
                file_path = Path(path)
                if not file_path.is_absolute():
                    file_path = self.output_dir / file_path  # ADD THIS LINE - combine with output_dir
                
                # Ensure the directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                return ToolResult(output=f"Successfully wrote {len(content)} characters to {file_path}")
            
            else:
                return ToolResult(error=f"Unknown action: {action}")
                
        except Exception as e:
            return ToolResult(error=f"Failed to write file: {str(e)}")
    

    def to_params(self) -> dict:
        """Return tool parameters for the API"""
        return {
            "name": self.name,
            "description": "Write content to a file at the specified path",
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["write"],
                        "description": "The action to perform (currently only 'write' is supported)"
                    },
                    "path": {
                        "type": "string",
                        "description": "The file path where content should be written (e.g., './output/test.py')"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    }
                },
                "required": ["action", "path", "content"]
            }
        }