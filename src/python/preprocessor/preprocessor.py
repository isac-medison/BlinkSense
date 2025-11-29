import cv2
from src.python.config.config import get_config

class Preprocessor:
    """
    Preprocessing module for Blink Detection
    Handles resizing, grayscale conversion, normalization
    """
    def __init__(self):
        self.config = get_config()
        self.clahe = cv2.createCLAHE(clipLimit=self.config.contrast, tileGridSize=(8, 8))

    def preprocess(self, frame):
        res = frame.copy()
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        res = cv2.GaussianBlur(res, (5, 5), 0)
        res = cv2.equalizeHist(res)
        res = self.clahe.apply(res)
        return res
