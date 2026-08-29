"""
Person Entry/Exit Tracker
"""

from typing import Dict


class PersonTracker:
    """
    Tracks people crossing a virtual horizontal line.
    """

    def __init__(self, line_y: int = 300):

        self.line_y = line_y

        # Stores the last known side of each tracked person
        self.person_side: Dict[int, str] = {}

        self.entry_count = 0
        self.exit_count = 0

    def update(self, track_id: int, center_y: int):
        """
        Update a tracked person's position.
        """

        current_side = "above" if center_y < self.line_y else "below"

        if track_id not in self.person_side:
            self.person_side[track_id] = current_side
            return

        previous_side = self.person_side[track_id]

        if previous_side == "above" and current_side == "below":
            self.entry_count += 1

        elif previous_side == "below" and current_side == "above":
            self.exit_count += 1

        self.person_side[track_id] = current_side