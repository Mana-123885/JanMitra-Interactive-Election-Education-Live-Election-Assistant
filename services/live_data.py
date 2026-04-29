import json
from datetime import datetime

class LiveDataService:
    def __init__(self, data_path="data/live_mock.json"):
        self.data_path = data_path
        
    def get_updates(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_last_updated_string(self):
        return datetime.now().strftime("%Y-%m-%d %I:%M %p")

live_data_service = LiveDataService()
