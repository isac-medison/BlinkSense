import logging
import cv2
import numpy as np
import mediapipe as mp

from src.python.utils import is_blink, calculate_EAR
from src.python.constants import MP_L_EYE, MP_R_EYE

class Detector:
    def __init__(self):
        self.ear = 0.5
        self.logger = logging.getLogger("detector")
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.net = cv2.dnn.readNetFromCaffe(
            "model/deploy.prototxt", "model/res10_300x300_ssd_iter_140000.caffemodel"
        )

    def detect(self, frame):
        if len(frame.shape) == 2 or frame.shape[2] == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        h, w = frame.shape[:2]

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            l_shape = np.array(
                [[int(landmarks[i].x * w), int(landmarks[i].y * h)] for i in MP_L_EYE]
            )
            r_shape = np.array(
                [[int(landmarks[i].x * w), int(landmarks[i].y * h)] for i in MP_R_EYE]
            )

            l_ear = calculate_EAR(l_shape)
            r_ear = calculate_EAR(r_shape)
            self.ear = (l_ear + r_ear) / 2


            # draw eyes
            # --- Draw left eye points ---
            for (x, y) in l_shape:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # --- Draw right eye points ---
            for (x, y) in r_shape:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        return frame
