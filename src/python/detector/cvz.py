import logging
from src.python.config.config import get_config
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from src.python.utils import is_blink

class Detector:
    def __init__(self):
        self.ear = 0.5
        self.prev_ear = 0.5
        self.blink_count = 0
        self.detector = FaceMeshDetector(maxFaces=1)
        self.config = get_config()
        self.logger = logging.getLogger("detector")
        self.idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        self.RIGHT_EYE = [33, 159, 158, 133, 153, 145]
        self.LEFT_EYE = [362, 380, 374, 263, 386, 385]

    def detect(self, frame):
        if frame is None or not hasattr(frame, "shape"):
            self.logger.error("Invalid frame: not a color image or imdecode returned None")
            return None

        if len(frame.shape) == 2:  # grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.shape[2] == 4:  # RGBA
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        result = self.detector.findFaceMesh(frame, draw=False)
        if result is None:
            self.logger.error("findFaceMesh returned None")
            return None

        if len(result) == 2:
            img, faces = result
        elif len(result) == 3:
            img, faces, _ = result
        else:
            self.logger.error(f"Unexpected findFaceMesh result length: {len(result)}")
            return None

        if faces:
            face = faces[0]  # беремо перше обличчя

            # Функція для обчислення EAR одного ока
            def get_eye_aspect_ratio(eye_points):
                p1, p2, p3, p4, p5, p6 = eye_points
                ver1 = ((p2[0] - p6[0]) ** 2 + (p2[1] - p6[1]) ** 2) ** 0.5
                ver2 = ((p3[0] - p5[0]) ** 2 + (p3[1] - p5[1]) ** 2) ** 0.5
                hor = ((p1[0] - p4[0]) ** 2 + (p1[1] - p4[1]) ** 2) ** 0.5
                return (ver1 + ver2) / (2.0 * hor)

            # Беремо точки очей по індексах FaceMesh
            right_eye = [face[i] for i in self.RIGHT_EYE]
            left_eye = [face[i] for i in self.LEFT_EYE]

            r_ear = get_eye_aspect_ratio(right_eye)
            l_ear = get_eye_aspect_ratio(left_eye)
            self.ear = (l_ear + r_ear) / 2

            # Детекція кліпання
            if is_blink(getattr(self, "prev_ear", None), self.ear):
                self.blink_count = getattr(self, "blink_count", 0) + 1

            self.prev_ear = self.ear

        return img
