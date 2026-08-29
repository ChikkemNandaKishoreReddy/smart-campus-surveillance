"""
Event Manager

Stores intrusion events.
Later these events will be inserted into SQLite.
"""

from datetime import datetime


class EventManager:

    def __init__(self):

        self.events = []
        self.event_counter = 1

    def add_intrusion(self, track_id, screenshot):

        event = {

            "event_id": self.event_counter,

            "event_type": "Intrusion",

            "track_id": track_id,

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "screenshot": screenshot,
        }

        self.events.append(event)

        self.event_counter += 1

        return event

    def get_events(self):

        return self.events