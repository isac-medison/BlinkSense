import logging
from src.python.config.config import get_config
import dlib
from imutils import face_utils

from src.python.utils import calculate_EAR,is_blink

(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']


class Detector:
    def __init__(self):
        self.ear = 0.5
        self.prev_ear = 0.5
        self.blink_count = 0
        self.config = get_config()
        self.logger = logging.getLogger("detector")
        self.landmark_predict = dlib.shape_predictor(
            'model/shape_predictor_68_face_landmarks.dat')
        self.detector = dlib.get_frontal_face_detector()


    def detect(self, frame):
        faces = self.detector(frame)
        for face in faces:
            shape = self.landmark_predict(frame, face)
            shape = face_utils.shape_to_np(shape)
            lefteye = shape[L_start: L_end]
            righteye = shape[R_start:R_end]
            left_EAR = calculate_EAR(lefteye)
            right_EAR = calculate_EAR(righteye)
            self.ear = (left_EAR + right_EAR) / 2
            if is_blink(self.prev_ear, self.ear):
                self.blink_count += 1
            self.prev_ear = self.ear
        return frame