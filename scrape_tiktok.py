from playwright.sync_api import sync_playwright
import time
import re

def scrape_tiktok_by_hashtag(hashtag: str, num_videos: int = 10):
    """
    Scrapes TikTok videos for a given hashtag using Playwright.

    Args:
        hashtag (str): The hashtag to search for.
        num_videos (int): The number of videos to scrape data for.

    Returns:
        list: A list of dictionaries, where each dictionary contains
              data for a scraped video.
    """
    videos_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"https://www.tiktok.com/tag/{hashtag}")

        # Scroll to load more videos
        for _ in range(num_videos // 5): # Approximate scrolling needed
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2) # Give content time to load

        video_elements = page.query_selector_all('div[data-e2e="video-card"]')

        for i, video_element in enumerate(video_elements[:num_videos]):
            try:
                video_data = {}

                # Get video URL
                video_data['video_url'] = video_element.query_selector('a').get_attribute('href')

                # Click on the video to open its page for more details
                video_element.click()
                page.wait_for_url(video_data['video_url'])
                time.sleep(3) # Wait for the video page to load

                # Get likes, shares, comments (xpath can be fragile, might need adjustment)
                likes_element = page.query_selector('div[data-e2e="like-count"]')
                video_data['likes'] = likes_element.inner_text() if likes_element else 'N/A'

                comments_element = page.query_selector('div[data-e2e="comment-count"]')
                video_data['comments'] = comments_element.inner_text() if comments_element else 'N/A'

                shares_element = page.query_selector('div[data-e2e="share-count"]')
                video_data['shares'] = shares_element.inner_text() if shares_element else 'N/A'

                # Views are often displayed on the video card, but sometimes on the video page too.
                # Let's try to get it from the video page if available, otherwise from the card
                views_element_page = page.query_selector('strong[data-e2e="view-count"]')
                if views_element_page:
                    video_data['views'] = views_element_page.inner_text()
                else:
                    # Try getting from the initial video card if not on the page
                    views_element_card = video_element.query_selector('strong[data-e2e="video-views"]')
                    video_data['views'] = views_element_card.inner_text() if views_element_card else 'N/A'


                # Get caption and hashtags
                caption_element = page.query_selector('div[data-e2e="video-caption"]')
                full_caption = caption_element.inner_text() if caption_element else ''
                video_data['caption'] = full_caption
                video_data['hashtags'] = re.findall(r"#(\w+)", full_caption)

                # Getting video length and music information requires more advanced techniques
                # involving inspecting network requests or deeper DOM analysis, which is
                # more complex and prone to breakage. We'll skip these for this basic script.
                video_data['video_length'] = 'N/A' # Placeholder
                video_data['music'] = 'N/A' # Placeholder

                videos_data.append(video_data)

                # Go back to the hashtag page
                page.go_back()
                time.sleep(2) # Wait for the previous page to load

            except Exception as e:
                print(f"Error scraping video {i}: {e}")
                # Go back if we navigated away
                if page.url != f"https://www.tiktok.com/tag/{hashtag}":
                     page.go_back()
                     time.sleep(2)
                continue # Continue to the next video

        browser.close()
    return videos_data

if __name__ == "__main__":
    # Example usage
    hashtag = "foryoupage"
    scraped_data = scrape_tiktok_by_hashtag(hashtag, num_videos=20)

    for video in scraped_data:
        print(video)