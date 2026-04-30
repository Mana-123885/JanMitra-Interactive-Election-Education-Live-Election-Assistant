import json
import feedparser
from datetime import datetime

class LiveDataService:
    def __init__(self, data_path="data/live_mock.json"):
        self.data_path = data_path
        self.rss_url = "https://news.google.com/rss/search?q=Indian+Elections+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
        
    def get_updates(self):
        try:
            # Try fetching real-time news from Google News
            feed = feedparser.parse(self.rss_url)
            if feed.entries:
                live_updates = []
                for entry in feed.entries[:10]: # Get top 10 updates
                    live_updates.append({
                        "id": entry.get("id", ""),
                        "state": "Live News",
                        "election_type": "Update",
                        "status": "Recent",
                        "date": entry.get("published", ""),
                        "description": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "source": entry.get("source", {}).get("title", "Google News")
                    })
                return live_updates
        except Exception as e:
            print(f"RSS Fetch Error: {e}")
            
        # Fallback to mock data if RSS fails
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_last_updated_string(self):
        return datetime.now().strftime("%Y-%m-%d %I:%M %p")

live_data_service = LiveDataService()
