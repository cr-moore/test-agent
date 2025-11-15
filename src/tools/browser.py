from anthropic.types.beta import BetaToolComputerUse20250124Param
from typing import Literal, TypedDict
from playwright.sync_api import Page, expect
# from playwright.async_api import Keyboard


OUTPUT_DIR = "../screenshots"
KEY_MAP = {
    "return": Keys.ENTER,
    "tab": Keys.TAB,
    "space": Keys.SPACE,
    "backspace": Keys.BACKSPACE,
    "escape": Keys.ESCAPE,
    "page_down": Keys.PAGE_DOWN,
    "page_up": Keys.PAGE_UP,
}

class BrowserTool:
    """
    Allows control and interactions with a browser
    """

    name: Literal["browser"] = "browser"
    api_type: Literal["computer_20250124"] = "computer_20250124"
    _screenshot_delay = 2.0
    screenshot_counter = 1

    def __init__(self, website_url):
        Page.goto(website_url)


