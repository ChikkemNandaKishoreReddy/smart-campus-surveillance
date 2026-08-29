"""
Settings Manager

Loads and saves application settings.
"""

import json
from pathlib import Path


class SettingsManager:

    def __init__(self):

        self.settings_path = Path("app/config/settings.json")

        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

        self.default_settings = {
            "confidence": 0.5,
            "camera_index": 0,
            "save_screenshots": True,
            "enable_logs": True,
            "auto_refresh": False,
            "refresh_interval": 10,
            "database_path": "data/database/events.db",
            "csv_path": "data/csv",
        }

        if not self.settings_path.exists():
            self.save(self.default_settings)

    def load(self):

        try:
            with open(self.settings_path, "r") as file:
                return json.load(file)

        except Exception:
            return self.default_settings

    def save(self, settings):

        with open(self.settings_path, "w") as file:
            json.dump(settings, file, indent=4)