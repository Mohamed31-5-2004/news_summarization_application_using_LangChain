import json
import os
from datetime import datetime


class UserManager:
    def __init__(self, path="user_data.json"):
        self.path = path
        self.data = {"preferences": [], "history": []}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"preferences": [], "history": []}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def add_preference(self, topic):
        if topic not in self.data["preferences"]:
            self.data["preferences"].append(topic)
            self._save()

    def remove_preference(self, topic):
        if topic in self.data["preferences"]:
            self.data["preferences"].remove(topic)
            self._save()

    def get_preferences(self):
        return list(self.data.get("preferences", []))

    def add_history(self, topic, results_count, summary_type):
        entry = {
            "topic": topic,
            "results_count": results_count,
            "summary_type": summary_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.data.setdefault("history", []).append(entry)
        self._save()

    def get_history(self, limit=50):
        return list(self.data.get("history", []))[-limit:]
