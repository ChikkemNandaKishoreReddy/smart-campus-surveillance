"""
Restricted Area Monitoring
"""


class RestrictedArea:

    def __init__(self):

        # Rectangle coordinates
        self.x1 = 450
        self.y1 = 100

        self.x2 = 620
        self.y2 = 350

    def draw(self, frame):

        import cv2

        cv2.rectangle(
            frame,
            (self.x1, self.y1),
            (self.x2, self.y2),
            (0, 0, 255),
            3,
        )

        cv2.putText(
            frame,
            "RESTRICTED AREA",
            (self.x1, self.y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

    def contains(self, center_x, center_y):

        return (
            self.x1 <= center_x <= self.x2
            and
            self.y1 <= center_y <= self.y2
        )