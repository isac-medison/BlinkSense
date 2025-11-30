import sys
import os
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

import cv2
from src.python.config.config import get_config
from src.python.preprocessor.preprocessor import Preprocessor
from src.python.detector.dnn_m import Detector

from src.python.utils import is_blink, put_custom_text

config = get_config()
prepr = Preprocessor()
detector = Detector()


def count_blinks_in_video(video_path, output_dir):
    detector.ear = 0
    cap = cv2.VideoCapture(video_path)

    # --- Create output path ---
    os.makedirs(output_dir, exist_ok=True)

    # Extract file name only
    file_name = os.path.basename(video_path)
    out_path = os.path.join(output_dir, f"processed_{file_name}")

    # --- Video writer settings ---
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    blink_count = 0
    prev_ear = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        # preprocess + detect
        frame = prepr.preprocess(frame)
        frame = detector.detect(frame)


        # blink counting
        if is_blink(prev_ear, detector.ear):
            blink_count += 1
        prev_ear = detector.ear
        put_custom_text(frame, detector.ear, blink_count)
        out.write(frame)


    cap.release()
    out.release()

    return blink_count, os.path.abspath(os.path.normpath(out_path))

def test_blink_count_failure_gap():
    video_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../data/videos")
    )

    output_dir = os.path.join(os.path.dirname(__file__), "../../../data/videos/processed")

    res = []
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    for video_file in video_files:
        video_path = os.path.join(video_dir, video_file)
        blink_count = count_blinks_in_video(video_path, output_dir)
        res.append(f"Video: {video_file}, Blinks: {blink_count}")

    for i in res:
        print(i)


if __name__ == "__main__":
    test_blink_count_failure_gap()
