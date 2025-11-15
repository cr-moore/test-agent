from typing import Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import asyncio
from pathlib import Path
import base64
from .base import ToolResult, BaseAnthropicTool


OUTPUT_DIR = Path("../screenshots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

KEY_MAP = {
    "return": "Enter",
    "tab": "Tab",
    "space": "Space",
    "backspace": "Backspace",
    "escape": "Escape",
    "page_down": "PageDown",
    "page_up": "PageUp",
}


class BrowserTool(BaseAnthropicTool):
    """
    Allows control and interactions with a browser
    """

    name = "browser"
    _screenshot_delay = 2.0
    screenshot_counter = 1

    def __init__(self, website_url: str, width: int = 1920, height: int = 1080):
        self.website_url = website_url
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.width = width
        self.height = height

    async def __call__(self, **kwargs) -> ToolResult:
        """Executes the tool with the given arguments."""
        action = kwargs.get("action")
        text = kwargs.get("text")
        x = kwargs.get("x")
        y = kwargs.get("y")
        url = kwargs.get("url")
        
        print(f"BrowserTool called: action={action}, x={x}, y={y}, text={text}")
        
        try:
            if action == "screenshot":
                return await self.take_screenshot()
            
            elif action == "mouse_move" and x is not None and y is not None:
                return await self.mouse_move(x, y)
            
            elif action == "click" and x is not None and y is not None:
                return await self.click(x, y)
            
            elif action == "type" and text:
                return await self.type_text(text)
            
            elif action == "key" and text:
                return await self.press_key(text)
            
            elif action == "scroll" and x is not None and y is not None:
                return await self.scroll(x, y)
            
            elif action == "navigate" and url:
                return await self.navigate(url)
            
            elif action == "get_content":
                return await self.get_page_content()
            
            elif action == "get_title":
                return await self.get_page_title()
            
            else:
                return ToolResult(error=f"Invalid action or missing parameters: action={action}")
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return ToolResult(error=f"Error executing {action}: {str(e)}")

    async def _get_viewport_size(self) -> tuple[int, int]:
        """Get current viewport size from the page"""
        width = await self.page.evaluate("window.innerWidth")
        height = await self.page.evaluate("window.innerHeight")
        return width, height

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def start(self) -> None:
        """Initialize the browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(
            viewport={'width': self.width, 'height': self.height}
        )
        self.page = await self.context.new_page()
        await self.page.goto(self.website_url)
        
        # Update width/height with actual viewport size
        self.width, self.height = await self._get_viewport_size()

    async def take_screenshot(self) -> ToolResult:
        """Take a screenshot and return as ToolResult"""
        await asyncio.sleep(self._screenshot_delay)
        screenshot_bytes = await self.page.screenshot(full_page=False)
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
        
        # Also save to disk
        screenshot_path = OUTPUT_DIR / f"screenshot_{self.screenshot_counter}.png"
        with open(screenshot_path, 'wb') as f:
            f.write(screenshot_bytes)
        self.screenshot_counter += 1
        print(f"Screenshot saved to: {screenshot_path}")
        
        return ToolResult(
            output=f"Screenshot taken and saved to {screenshot_path}. Viewport: {self.width}x{self.height}",
            base64_image=screenshot_b64
        )

    async def click(self, x: int, y: int) -> ToolResult:
        """Click at coordinates"""
        await self.page.mouse.click(x, y)
        return ToolResult(output=f"Clicked at ({x}, {y})")

    async def type_text(self, text: str) -> ToolResult:
        """Type text at current cursor position"""
        await self.page.keyboard.type(text)
        return ToolResult(output=f"Typed: {text}")

    async def press_key(self, key: str) -> ToolResult:
        """Press a key"""
        playwright_key = KEY_MAP.get(key, key)
        await self.page.keyboard.press(playwright_key)
        return ToolResult(output=f"Pressed key: {key}")

    async def scroll(self, x: int, y: int) -> ToolResult:
        """Scroll by x, y pixels"""
        await self.page.evaluate(f"window.scrollBy({x}, {y})")
        return ToolResult(output=f"Scrolled by ({x}, {y})")

    async def mouse_move(self, x: int, y: int) -> ToolResult:
        """Move mouse to coordinates"""
        await self.page.mouse.move(x, y)
        return ToolResult(output=f"Mouse moved to ({x}, {y})")

    async def navigate(self, url: str) -> ToolResult:
        """Navigate to a new URL"""
        await self.page.goto(url)
        return ToolResult(output=f"Navigated to: {url}")

    async def get_page_content(self) -> ToolResult:
        """Get the current page HTML content"""
        content = await self.page.content()
        return ToolResult(output=content[:1000])  # Truncate for brevity

    async def get_page_title(self) -> ToolResult:
        """Get the current page title"""
        title = await self.page.title()
        return ToolResult(output=f"Page title: {title}")

    def to_params(self) -> dict[str, Any]:
        """Convert object to API parameters for custom tool."""
        return {
            "name": self.name,
            "description": "Control a web browser to navigate, click, type, and take screenshots",
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "screenshot",
                            "click",
                            "type",
                            "key",
                            "navigate",
                            "scroll",
                            "mouse_move",
                            "get_content",
                            "get_title"
                        ],
                        "description": "The action to perform"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to type or key to press"
                    },
                    "x": {
                        "type": "integer",
                        "description": "X coordinate for click or mouse move"
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y coordinate for click or mouse move"
                    },
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to"
                    }
                },
                "required": ["action"]
            }
        }

    async def close(self) -> None:
        """Clean up resources"""
        try:
            if self.page:
                await self.page.close()
        except Exception as e:
            print(f"Error closing page: {e}")

        try:
            if self.context:
                await self.context.close()
        except Exception as e:
            print(f"Error closing context: {e}")

        try:
            if self.browser:
                await self.browser.close()
        except Exception as e:
            print(f"Error closing browser: {e}")

        try:
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Error stopping playwright: {e}")

        # Give time for cleanup
        await asyncio.sleep(0.5)