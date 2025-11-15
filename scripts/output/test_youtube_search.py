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
        
        # Navigate to YouTube
        page.goto('https://www.youtube.com')
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Take initial screenshot
        page.screenshot(path='./output/screenshots/youtube_homepage.png')
        
        # Click on search bar
        search_box = page.locator('input[name="search_query"]')
        search_box.click()
        
        # Type 'lofi music' in the search bar
        search_box.fill('lofi music')
        
        # Press Enter to search
        search_box.press('Enter')
        
        # Wait for search results to load
        page.wait_for_load_state('networkidle')
        time.sleep(2)  # Additional wait for results to render
        
        # Take screenshot of search results
        page.screenshot(path='./output/screenshots/youtube_search_results.png')
        
        # Verify search results appear
        # Check if the search term is in the search box
        search_value = search_box.input_value()
        assert 'lofi music' in search_value.lower(), f"Expected 'lofi music' in search box, but got '{search_value}'"
        
        # Verify that video results are displayed
        video_results = page.locator('ytd-video-renderer, ytd-playlist-renderer, ytd-radio-renderer')
        expect(video_results.first).to_be_visible(timeout=10000)
        
        # Count the number of results
        results_count = video_results.count()
        assert results_count > 0, f"Expected search results to appear, but found {results_count} results"
        
        print(f"✓ Test passed: Found {results_count} search results for 'lofi music'")
        
        # Close browser
        browser.close()

if __name__ == "__main__":
    test_youtube_search_lofi_music()
    print("Test completed successfully!")
