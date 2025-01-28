import requests
import json
import time
import schedule
from bs4 import BeautifulSoup

# Configuration
BLOG_URL = "https://blog.naver.com/ranto28"
LAST_ARTICLE_FILE = "last_article.json"
DISCORD_WEBHOOK = "YOUR_DISCORD_WEBHOOK_URL"  # Replace with your webhook
SLACK_WEBHOOK = "YOUR_SLACK_WEBHOOK_URL"  # Replace with your webhook

def get_latest_article():
    """Fetches the latest article title and link from the blog."""
    response = requests.get(BLOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Modify this selector based on actual blog structure
    latest_post = soup.find("a", class_="some-class")  # Update class name accordingly
    if latest_post:
        return {
            "title": latest_post.text.strip(),
            "link": latest_post["href"]
        }
    return None

def load_last_article():
    """Loads the last checked article from local storage."""
    try:
        with open(LAST_ARTICLE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_last_article(article):
    """Saves the latest article to local storage."""
    with open(LAST_ARTICLE_FILE, "w") as f:
        json.dump(article, f)

def send_notification(article):
    """Sends a notification to Discord and Slack."""
    message = f"New Blog Post: {article['title']}\n{article['link']}"
    
    if DISCORD_WEBHOOK:
        requests.post(DISCORD_WEBHOOK, json={"content": message})
    if SLACK_WEBHOOK:
        requests.post(SLACK_WEBHOOK, json={"text": message})

def check_for_new_article():
    """Checks for a new blog post and sends a notification if found."""
    latest_article = get_latest_article()
    if not latest_article:
        print("Could not fetch latest article.")
        return

    last_article = load_last_article()
    if not last_article or latest_article["title"] != last_article["title"]:
        print("New article detected! Sending notification...")
        send_notification(latest_article)
        save_last_article(latest_article)
    else:
        print("No new articles found.")

# Schedule to run every 2 hours
schedule.every(2).hours.do(check_for_new_article)

if __name__ == "__main__":
    print("Starting blog checker...")
    check_for_new_article()  # Initial check
    while True:
        schedule.run_pending()
        time.sleep(60)