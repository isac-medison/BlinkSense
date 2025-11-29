import sys
import os
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

import cv2
from src.python.config.config import get_config
from src.python.preprocessor.preprocessor import Preprocessor
from src.python.detector.dnn_m import Detector

from src.python.utils import is_blink

config = get_config()
prepr = Preprocessor()
detector = Detector()

def count_blinks_in_video(video_path):
    detector.ear = 0
    cap = cv2.VideoCapture(video_path)
    blink_count = 0
    prev_ear = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        frame = prepr.preprocess(frame)
        frame = detector.detect(frame)
        if is_blink(prev_ear, detector.ear):
            blink_count += 1
        prev_ear = detector.ear
    cap.release()
    return blink_count


def test_blink_count_failure_gap():
    video_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../data/videos")
    )
    res = []
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        blink_count = count_blinks_in_video(video_path)
        res.append(f"Video: {video_file}, Blinks: {blink_count}")

    for i in res:
        print(i)


if __name__ == "__main__":
    test_blink_count_failure_gap()
