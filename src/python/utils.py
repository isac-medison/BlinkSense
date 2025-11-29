import cv2
from math import sqrt
from src.python.config.config import get_config
import numpy as np
import time

config = get_config()

def calculate_EAR(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_eye_aspect_ratio(eye_landmarks):
    vertical1 = euclidean(eye_landmarks[1], eye_landmarks[5])
    vertical2 = euclidean(eye_landmarks[2], eye_landmarks[4])
    horizontal = euclidean(eye_landmarks[0], eye_landmarks[3])
    return (vertical1 + vertical2) / (2.0 * horizontal)

def euclidean(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def put_custom_text(frame, ear, blinks):
    cv2.putText(frame, f"EAR: {ear:.2f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Blinks per {config.blink_time_window}s.: {blinks} ", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 0), 2)

def is_blink(prev_ear, ear):
    current_delta = prev_ear - ear
    return current_delta > config.ear_delta and ear < config.ear_trash

def get_time():
    return int(time.time())
