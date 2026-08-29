import cv2
from ultralytics import YOLO

from app.roi.restricted_area import RestrictedArea
from app.tracking.tracker import PersonTracker
from app.utils.logger import logger
from app.utils.screenshot import ScreenshotManager
from app.utils.event_manager import EventManager
from app.database.database import DatabaseManager
from app.analytics.analytics import Analytics

class YOLODetector:

    PERSON_CLASS = 0

    def __init__(self):

        logger.info("Loading YOLO...")

        self.model = YOLO("yolov8n.pt")

        self.tracker = PersonTracker()

        self.restricted_area = RestrictedArea()

        self.screenshot_manager = ScreenshotManager()

        self.event_manager = EventManager()

        self.database = DatabaseManager()

        logger.info("YOLO Loaded.")

    def start_detection(self):

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            raise RuntimeError("Cannot open webcam.")

        while True:

            success, frame = cap.read()

            if not success:
                break

            results = self.model.track(
                frame,
                persist=True,
                classes=[self.PERSON_CLASS],
                verbose=False,
            )

            self.restricted_area.draw(frame)

            cv2.line(
                frame,
                (0, self.tracker.line_y),
                (frame.shape[1], self.tracker.line_y),
                (255, 0, 255),
                3,
            )

            people_count = 0
            intrusion_detected = False

            if results and results[0].boxes is not None:

                intrusion_track_id = None

                for box in results[0].boxes:

                    if box.id is None:
                        continue

                    people_count += 1

                    track_id = int(box.id[0])

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    self.tracker.update(track_id, center_y)

                    intrusion = self.restricted_area.contains(
                        center_x,
                        center_y,
                    )

                    if intrusion:
                        intrusion_detected = True
                        intrusion_track_id = track_id

                    confidence = float(box.conf[0])

                    color = (0, 0, 255) if intrusion else (0, 255, 0)

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        color,
                        2,
                    )

                    cv2.putText(
                        frame,
                        f"ID:{track_id} {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )

                    cv2.circle(
                        frame,
                        (center_x, center_y),
                        4,
                        color,
                        -1,
                    )

            if intrusion_detected:

                filename = self.screenshot_manager.save_intrusion(frame)

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

                cv2.putText(
                    frame,
                    "INTRUSION DETECTED",
                    (20, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3,
                )

            else:

                self.screenshot_manager.reset()

            cv2.putText(
                frame,
                f"People : {people_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Entry : {self.tracker.entry_count}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Exit : {self.tracker.exit_count}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

            cv2.imshow("Smart Campus Surveillance", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                logger.info("Detection stopped.")
                logger.info("Latest Detection History:")
                events = self.database.get_latest_events()
                for event in events:
                    logger.info(dict(event))
                logger.info("Searching Track ID 1")
                results = self.database.get_events_by_track(1)
                for row in results:
                    logger.info(dict(row))
                csv_file = self.database.export_csv()
                logger.info("CSV Exported: %s", csv_file)
                analytics = Analytics()

                logger.info("========== Analytics ==========")

                summary = analytics.dashboard_summary()

                for key, value in summary.items():
                    logger.info("%s : %s", key, value)
                logger.info("Recent Events:")
                for event in analytics.recent_events():
                    logger.info(event)
                break

        cap.release()

        self.database.close()

        cv2.destroyAllWindows()