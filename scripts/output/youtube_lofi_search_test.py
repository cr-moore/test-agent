from playwright.sync_api import sync_playwright, expect
import time

def test_youtube_lofi_search():
    """
    Test case: Search for 'lofi music' on YouTube and verify search results appear
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # Navigate to YouTube (assumed to already be on youtube.com based on test context)
        page.goto("https://www.youtube.com")
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Click on the search bar
        page.click('input[name="search_query"]')
        
        # Type 'lofi music' in the search bar
        page.fill('input[name="search_query"]', 'lofi music')
        
        # Press Enter to search
        page.keyboard.press('Enter')
        
        # Wait for search results to load
        page.wait_for_load_state("networkidle")
        
        # Verify search results appear by checking for video thumbnails and titles
        # Wait for the results container to be visible
        page.wait_for_selector('ytd-video-renderer', timeout=10000)
        
        # Verify that search query is in the search box
        search_input = page.locator('input[name="search_query"]')
        expect(search_input).to_have_value('lofi music')
        
        # Verify that video results are present
        video_results = page.locator('ytd-video-renderer')
        expect(video_results.first).to_be_visible()
        
        # Optional: Verify filter buttons are visible (All, Shorts, Videos, etc.)
        filter_chips = page.locator('yt-chip-cloud-chip-renderer')
        expect(filter_chips.first).to_be_visible()
        
        print("Test passed: Search results for 'lofi music' appeared successfully")
        
        # Take a screenshot for verification
        page.screenshot(path='./output/youtube_search_results.png')
        
        # Close browser
        browser.close()

if __name__ == "__main__":
    test_youtube_lofi_search()
