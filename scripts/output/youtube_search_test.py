from playwright.sync_api import sync_playwright, expect
import time

def test_youtube_search_lofi_music():
    """
    Test case: Search for 'lofi music' on YouTube and verify search results appear
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        # Navigate to YouTube (assuming we're already on youtube.com as per instructions)
        page.goto('https://www.youtube.com')
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Click on search bar
        search_box = page.locator('input[name="search_query"]')
        search_box.click()
        
        # Type 'lofi music' in the search bar
        search_box.fill('lofi music')
        
        # Press Enter to submit search
        search_box.press('Enter')
        
        # Wait for search results to load
        page.wait_for_load_state('networkidle')
        time.sleep(2)  # Additional wait for results to fully render
        
        # Verify search results appear
        # Check that the URL contains the search query
        expect(page).to_have_url(lambda url: 'search_query=lofi+music' in url or 'lofi%20music' in url)
        
        # Verify filter tabs are visible (indicates we're on search results page)
        filters = page.locator('#filter-menu')
        expect(filters).to_be_visible()
        
        # Verify at least one video result is visible
        video_results = page.locator('ytd-video-renderer')
        expect(video_results.first).to_be_visible()
        
        print("✓ Search functionality test passed!")
        print("✓ Search query 'lofi music' was successfully entered")
        print("✓ Search results page loaded")
        print("✓ Video results are visible")
        
        # Close browser
        browser.close()

if __name__ == "__main__":
    test_youtube_search_lofi_music()
