"""
AI-Powered Smart Campus Surveillance System
Main Entry Point

Author: Nandu
"""

from app.detection.detector import YOLODetector
from app.utils.logger import logger
from app.analytics.analytics import Analytics

def main():
    """
    Main application entry point.
    """
    try:
        logger.info("Starting Smart Campus Surveillance System...")

        detector = YOLODetector()
        detector.start_detection()
        analytics = Analytics()

        analytics.generate_charts()
        logger.info("Analytics charts generated.")
        
    except Exception as error:
        logger.exception("Application crashed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

