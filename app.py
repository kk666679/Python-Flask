import asyncio
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from playwright.async_api import async_playwright

app = Flask(__name__)
CORS(app)  # Allow React Frontend to connect

# Function to scrape trending hashtags from TikTok
async def scrape_tiktok_trends():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()  # Or p.firefox.launch() or p.webkit.launch()
            page = await browser.new_page()
            await page.goto("https://www.tiktok.com/explore")  # Go to TikTok Explore
            await asyncio.sleep(3)
            trends = await page.query_selector_all("xpath=//strong[contains(text(),'#')]")
            trending_hashtags = []
            for trend in trends:
                text = await trend.inner_text()
                trending_hashtags.append(text.replace(' ', ''))
            await browser.close()
            return trending_hashtags

    except Exception as e:
        print(f"Error scraping TikTok trends: {e}")
        return ["Error retrieving trends"]


async def fetch_trending_hashtags():
    trends = await scrape_tiktok_trends()
    return trends


# Placeholder function for video analysis
def analyze_video(video_data):
    # TODO: Implement the actual video analysis logic
    return {"virality_score": 75, "feedback": "Good video!"}


@app.route("/api/trends", methods=["GET"])
async def get_trends():
    trends = await fetch_trending_hashtags()
    return jsonify({"trends": trends[:10]})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    # Assuming video data is sent in the request body
    video_data = request.get_json()
    result = analyze_video(video_data)
    return jsonify(result)

@app.route('/')
def home():
    return "ViralBoost API Running!"

if __name__ == '__main__':
    # Consider using environment variables for debug mode in production
    app.run(debug=True)