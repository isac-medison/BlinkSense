
import logging
from src.python.config.config import get_config
import cv2
import dlib
from imutils import face_utils
from src.python.utils import is_blink, calculate_EAR
from src.python.constants import L_start, L_end, R_start, R_end


class Detector:
    def __init__(self):
        self.ear = 0.5
        self.prev_ear = 0.5
        self.blink_count = 0
        self.config = get_config()
        self.logger = logging.getLogger("detector")
        self.landmark_predict = dlib.shape_predictor(
            'model/shape_predictor_68_face_landmarks.dat')
        # Load DNN face detector
        self.net = cv2.dnn.readNetFromCaffe(
            'model/deploy.prototxt',
            'model/res10_300x300_ssd_iter_140000.caffemodel'
        )

    def detect(self, frame):
        if len(frame.shape) == 2 or frame.shape[2] == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x1, y1, x2, y2) = box.astype("int")
                rect = dlib.rectangle(x1, y1, x2, y2)
                shape = self.landmark_predict(frame, rect)
                shape = face_utils.shape_to_np(shape)
                l_shape = shape[L_start:L_end]
                r_shape = shape[R_start:R_end]
                l_ear = calculate_EAR(l_shape)
                r_ear = calculate_EAR(r_shape)
                self.ear = (l_ear + r_ear) / 2
                if is_blink(self.prev_ear, self.ear):
                    self.blink_count += 1
                self.prev_ear = self.ear
        return frame
