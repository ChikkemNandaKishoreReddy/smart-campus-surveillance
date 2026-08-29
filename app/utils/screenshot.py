"""
Screenshot Manager
"""

from datetime import datetime
from pathlib import Path

import cv2

from app.utils.logger import logger


class ScreenshotManager:

    def __init__(self):

        self.output_dir = Path("data/screenshots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.intrusion_active = False

    def save_intrusion(self, frame):

        if self.intrusion_active:
            return None

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = f"intrusion_{timestamp}.jpg"

        full_path = self.output_dir / filename

        cv2.imwrite(str(full_path), frame)

        logger.info("Screenshot saved: %s", full_path)

        self.intrusion_active = True

        return filename

    def reset(self):

        self.intrusion_active = False