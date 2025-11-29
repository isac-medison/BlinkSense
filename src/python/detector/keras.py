import logging
from src.python.config.config import get_config
import numpy as np
import cv2
import dlib
from imutils import face_utils
from keras.models import load_model

from src.python.utils import is_blink
IMG_SIZE = (34, 26)

def crop_eye(img, eye_points):
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]
    margin_x, margin_y = w / 2, h / 2
    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)
    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int_)
    eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]
    return eye_img, eye_rect

class Detector:
    def __init__(self):
        self.ear = 0.5
        self.prev_ear = 0.5
        self.blink_count = 0
        self.config = get_config()
        self.logger = logging.getLogger("detector")

        self.model = load_model('model/2018_12_17_22_58_35.h5',compile=False)
        self.model.summary()
        self.config = get_config()
        self.logger = logging.getLogger("detector")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')

    def detect(self, frame):
        if len(frame.shape) == 2 or frame.shape[2] == 1:
            img = frame
        else:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector(img)

        for face in faces:
            shapes = self.predictor(img, face)
            shapes = face_utils.shape_to_np(shapes)

            eye_img_l, eye_rect_l = crop_eye(img, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(img, eye_points=shapes[42:48])

            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)

            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

            pred_l = self.model.predict(eye_input_l, verbose=0)
            pred_r = self.model.predict(eye_input_r, verbose=0)

            self.ear = float(np.squeeze((pred_l + pred_r) / 2))

            if is_blink(self.prev_ear, self.ear):
                self.blink_count += 1

            self.prev_ear = self.ear



        return img
