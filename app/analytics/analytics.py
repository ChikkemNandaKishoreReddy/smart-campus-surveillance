"""
Analytics Module
"""

from collections import Counter

from app.database.database import DatabaseManager

import os
import matplotlib.pyplot as plt

class Analytics:

    def __init__(self):
        self.database = DatabaseManager()

    def total_events(self):
        return len(self.database.get_all_events())

    def total_intrusions(self):
        return len(self.database.get_events_by_type("Intrusion"))

    def unique_people(self):
        events = self.database.get_all_events()
        return len({event["track_id"] for event in events})

    def latest_event(self):
        events = self.database.get_latest_events(1)
        return dict(events[0]) if events else None

    def recent_events(self, limit=5):
        events = self.database.get_latest_events(limit)
        return [dict(event) for event in events]
    
    def get_all_events(self):
        """
        Return all events from the database.
        """
        events = self.database.get_all_events()
        return [dict(event) for event in events]

    def daily_statistics(self):
        events = self.database.get_all_events()

        stats = {}

        for event in events:
            date = event["timestamp"].split()[0]
            stats[date] = stats.get(date, 0) + 1

        return stats

    def hourly_statistics(self):
        events = self.database.get_all_events()

        stats = {}

        for event in events:
            hour = event["timestamp"][11:13]
            stats[hour] = stats.get(hour, 0) + 1

        return dict(sorted(stats.items()))

    def track_statistics(self):
        events = self.database.get_all_events()

        counter = Counter()

        for event in events:
            counter[event["track_id"]] += 1

        return dict(counter)

    def dashboard_summary(self):
        return {
            "total_events": self.total_events(),
            "total_intrusions": self.total_intrusions(),
            "unique_people": self.unique_people(),
            "latest_event": self.latest_event(),
            "daily_statistics": self.daily_statistics(),
            "hourly_statistics": self.hourly_statistics(),
            "track_statistics": self.track_statistics(),
        }
    def generate_charts(self):
        """
        Generate analytics charts.
        """

        os.makedirs("data/analytics", exist_ok=True)

        # -----------------------------
        # Daily Events
        # -----------------------------

        daily = self.daily_statistics()

        if daily:

            plt.figure(figsize=(8, 5))

            plt.bar(daily.keys(), daily.values())

            plt.title("Daily Intrusions")

            plt.xlabel("Date")

            plt.ylabel("Count")

            plt.tight_layout()

            plt.savefig("data/analytics/daily_events.png")

            plt.close()

        # -----------------------------
        # Hourly Events
        # -----------------------------

        hourly = self.hourly_statistics()

        if hourly:
            plt.figure(figsize=(8, 5))

            plt.bar(hourly.keys(), hourly.values())

            plt.title("Hourly Intrusions")

            plt.xlabel("Hour")

            plt.ylabel("Count")

            plt.tight_layout()

            plt.savefig("data/analytics/hourly_events.png")

            plt.close()

        # -----------------------------
        # Track Statistics
        # -----------------------------

        tracks = self.track_statistics()

        if tracks:
            labels = [str(k) for k in tracks.keys()]

            values = list(tracks.values())

            plt.figure(figsize=(8, 5))

            plt.bar(labels, values)

            plt.title("Intrusions by Track ID")

            plt.xlabel("Track ID")

            plt.ylabel("Intrusions")

            plt.tight_layout()

            plt.savefig("data/analytics/track_statistics.png")

            plt.close()

    