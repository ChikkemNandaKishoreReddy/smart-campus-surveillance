"""
YOLOv8 Detection Module

Smart Campus Surveillance System

This module provides the main real-time detection pipeline.

The production model used by the application is the best-performing
fine-tuned YOLOv8n model obtained from the project's model comparison.

Responsibilities:
    - Load the fine-tuned YOLOv8n model
    - Detect persons from webcam frames
    - Track detected persons
    - Count people
    - Count entries and exits
    - Monitor the restricted area
    - Capture intrusion screenshots
    - Log intrusion events
    - Store events in SQLite
    - Export detection history
    - Generate analytics summaries
"""

from pathlib import Path

import cv2
from ultralytics import YOLO

from app.analytics.analytics import Analytics
from app.database.database import DatabaseManager
from app.roi.restricted_area import RestrictedArea
from app.tracking.tracker import PersonTracker
from app.utils.event_manager import EventManager
from app.utils.logger import logger
from app.utils.screenshot import ScreenshotManager


class YOLODetector:
    """Main real-time YOLOv8 surveillance detector."""

    # YOLO class ID for the Person class.
    PERSON_CLASS = 0

    def __init__(self):
        """Initialize the surveillance detection system."""

        logger.info("Initializing YOLO detector.")

        # ---------------------------------------------------------
        # Project paths
        # ---------------------------------------------------------

        self.project_root = Path(__file__).resolve().parents[2]

        # The fine-tuned model is the best-performing model
        # selected from the three-model comparison experiment.
        self.model_path = (
            self.project_root
            / "runs"
            / "finetuned_yolov8n"
            / "weights"
            / "best.pt"
        )

        # ---------------------------------------------------------
        # Load final production model
        # ---------------------------------------------------------

        self.model = self._load_model()

        # ---------------------------------------------------------
        # Initialize project components
        # ---------------------------------------------------------

        self.tracker = PersonTracker()

        self.restricted_area = RestrictedArea()

        self.screenshot_manager = ScreenshotManager()

        self.event_manager = EventManager()
        # Track IDs that have already generated an intrusion
        # event during their current presence inside the
        # restricted area.
        self.active_intrusion_tracks = set()

        self.database = DatabaseManager()

        logger.info("YOLO detector initialized successfully.")

    def _load_model(self):
        """
        Load the final fine-tuned YOLOv8n model.

        Returns:
            YOLO: Loaded Ultralytics YOLO model.

        Raises:
            FileNotFoundError: If the trained model does not exist.
        """

        print("=" * 60)
        print("LOADING BEST-PERFORMING YOLOV8N MODEL")
        print("=" * 60)
        print(f"Model path: {self.model_path}")
        print("Model type: Fine-tuned YOLOv8n")
        print("Source: Custom dataset + pretrained YOLOv8n")
        print("=" * 60)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Fine-tuned YOLOv8n model not found: {self.model_path}"
            )

        model = YOLO(str(self.model_path))

        print("Fine-tuned YOLOv8n loaded successfully.")

        return model

    def _process_detections(self, frame, results):
        """
        Process detected persons in the current frame.

        Args:
            frame: Current OpenCV video frame.
            results: YOLO tracking results.

        Returns:
            tuple:
                people_count,
                intrusion_detected,
                intrusion_track_id
        """

        people_count = 0
        intrusion_detected = False
        intrusion_track_id = None

        # Track IDs currently visible inside the restricted area.
        current_intrusion_tracks = set()

        if not results or results[0].boxes is None:
            # No detections means no person is currently
            # visible inside the restricted area.
            self.active_intrusion_tracks.clear()

            return (
                people_count,
                intrusion_detected,
                intrusion_track_id,
            )

        for box in results[0].boxes:

            # Tracking IDs are required for the project's
            # person tracking and entry/exit functionality.
            if box.id is None:
                continue

            people_count += 1

            track_id = int(box.id[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0],
            )

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Update persistent person tracking.
            self.tracker.update(
                track_id,
                center_y,
            )

            # Check whether the person is inside
            # the restricted area.
            intrusion = self.restricted_area.contains(
                center_x,
                center_y,
            )

            if intrusion:
                current_intrusion_tracks.add(track_id)

                # Only report an intrusion event when this
                # track first enters the restricted area.
                if track_id not in self.active_intrusion_tracks:
                    intrusion_detected = True
                    intrusion_track_id = track_id

            confidence = float(box.conf[0])

            # Red bounding box = intrusion.
            # Green bounding box = normal detection.
            color = (
                (0, 0, 255)
                if intrusion
                else (0, 255, 0)
            )

            # Draw bounding box.
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2,
            )

            # Draw ID and confidence.
            cv2.putText(
                frame,
                f"ID:{track_id} {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

            # Draw person's center point.
            cv2.circle(
                frame,
                (center_x, center_y),
                4,
                color,
                -1,
            )

        # Update active intrusion tracks.
        #
        # Tracks that are still inside remain active.
        # Tracks that have left are removed so that a future
        # re-entry can generate a new intrusion event.
        self.active_intrusion_tracks.intersection_update(
            current_intrusion_tracks
        )

        if intrusion_detected:
            self.active_intrusion_tracks.add(
                intrusion_track_id
            )

        return (
            people_count,
            intrusion_detected,
            intrusion_track_id,
        )

    def _handle_intrusion(
        self,
        frame,
        intrusion_detected,
        intrusion_track_id,
    ):
        """
        Handle intrusion screenshot capture and database logging.

        Args:
            frame: Current OpenCV video frame.
            intrusion_detected: Whether a new intrusion occurred.
            intrusion_track_id: Track ID responsible for intrusion.
        """

        if intrusion_detected:

            filename = self.screenshot_manager.save_intrusion(
                frame
            )

            if filename is not None:

                event = self.event_manager.add_intrusion(
                    intrusion_track_id,
                    filename,
                )

                logger.info(event)

                self.database.insert_event(
                    event["event_type"],
                    event["track_id"],
                    event["timestamp"],
                    event["screenshot"],
                )

        # Display the intrusion warning only when a new
        # intrusion was detected in the current frame.
        if intrusion_detected:
            cv2.putText(
                frame,
                "INTRUSION DETECTED",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )

    def _draw_interface(self, frame, people_count):
        """
        Draw surveillance information on the video frame.

        Args:
            frame: Current OpenCV video frame.
            people_count: Number of currently tracked people.
        """

        # Draw restricted area.
        self.restricted_area.draw(frame)

        # Draw entry/exit counting line.
        cv2.line(
            frame,
            (0, self.tracker.line_y),
            (frame.shape[1], self.tracker.line_y),
            (255, 0, 255),
            3,
        )

        # Current people count.
        cv2.putText(
            frame,
            f"People : {people_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        # Entry count.
        cv2.putText(
            frame,
            f"Entry : {self.tracker.entry_count}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        # Exit count.
        cv2.putText(
            frame,
            f"Exit : {self.tracker.exit_count}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    def _generate_session_summary(self):
        """Generate and log the detection session summary."""

        logger.info("Detection stopped.")

        # ---------------------------------------------------------
        # Detection history
        # ---------------------------------------------------------

        logger.info("Latest Detection History:")

        events = self.database.get_latest_events()

        for event in events:
            logger.info(dict(event))

        # ---------------------------------------------------------
        # Track-specific search
        # ---------------------------------------------------------

        logger.info("Searching Track ID 1")

        track_events = self.database.get_events_by_track(1)

        for row in track_events:
            logger.info(dict(row))

        # ---------------------------------------------------------
        # CSV export
        # ---------------------------------------------------------

        csv_file = self.database.export_csv()

        logger.info("CSV Exported: %s", csv_file)

        # ---------------------------------------------------------
        # Analytics
        # ---------------------------------------------------------

        analytics = Analytics()

        logger.info("========== Analytics ==========")

        summary = analytics.dashboard_summary()

        for key, value in summary.items():
            logger.info("%s : %s", key, value)

        logger.info("Recent Events:")

        for event in analytics.recent_events():
            logger.info(event)

    def start_detection(self):
        """Start the real-time webcam surveillance system."""

        cap = None

        try:
            # -----------------------------------------------------
            # Open webcam
            # -----------------------------------------------------

            cap = cv2.VideoCapture(
                0,
                cv2.CAP_DSHOW,
            )

            if not cap.isOpened():
                raise RuntimeError(
                    "Cannot open webcam."
                )

            logger.info(
                "Webcam opened successfully."
            )

            # -----------------------------------------------------
            # Main detection loop
            # -----------------------------------------------------

            while True:

                success, frame = cap.read()

                if not success:
                    logger.warning(
                        "Failed to read frame from webcam."
                    )
                    break

                # -------------------------------------------------
                # YOLO person detection + tracking
                # -------------------------------------------------

                results = self.model.track(
                    frame,
                    persist=True,
                    classes=[self.PERSON_CLASS],
                    verbose=False,
                )

                # -------------------------------------------------
                # Process detections
                # -------------------------------------------------

                (
                    people_count,
                    intrusion_detected,
                    intrusion_track_id,
                ) = self._process_detections(
                    frame,
                    results,
                )

                # -------------------------------------------------
                # Intrusion handling
                # -------------------------------------------------

                self._handle_intrusion(
                    frame,
                    intrusion_detected,
                    intrusion_track_id,
                )

                # -------------------------------------------------
                # Draw interface
                # -------------------------------------------------

                self._draw_interface(
                    frame,
                    people_count,
                )

                # -------------------------------------------------
                # Display frame
                # -------------------------------------------------

                cv2.imshow(
                    "Smart Campus Surveillance",
                    frame,
                )

                # Press Q to stop.
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self._generate_session_summary()
                    break

        except Exception:
            logger.exception(
                "Error occurred during detection."
            )
            raise

        finally:
            # -----------------------------------------------------
            # Always release resources
            # -----------------------------------------------------

            if cap is not None:
                cap.release()

            self.database.close()

            cv2.destroyAllWindows()

            logger.info(
                "Detection resources released."
            )
