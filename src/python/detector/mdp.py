import logging
from src.python.config.config import get_config
import cv2
from mediapipe import solutions
from math import sqrt
import numpy as np
from src.python.utils import get_eye_aspect_ratio, is_blink



def euclidean(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class Detector:
    blink_counter = 0  # Лічильник для підрядних кліпань

    def __init__(self):
        self.ear = 0.5
        self.prev_ear = 0.5
        self.blink_count = 0
        self.config = get_config()
        self.logger = logging.getLogger("detector")
        self.mp_face_mesh = solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
        self.RIGHT_EYE = [33, 159, 158, 133, 153, 145]
        self.LEFT_EYE = [362, 380, 374, 263, 386, 385]


    def detect(self, frame):
        h, w = frame.shape[:2]
        if frame.dtype != np.uint8:
            frame = (frame * 255).clip(0, 255).astype(np.uint8)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            def get_landmark_points(indices):
                return [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]

            right_eye = get_landmark_points(self.RIGHT_EYE)
            left_eye = get_landmark_points(self.LEFT_EYE)

            r_ear = get_eye_aspect_ratio(right_eye)
            l_ear = get_eye_aspect_ratio(left_eye)
            self.ear = (l_ear + r_ear) / 2

            if is_blink(self.prev_ear, self.ear):
                self.blink_count += 1
            self.prev_ear = self.ear
        return frame

