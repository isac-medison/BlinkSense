from imutils import face_utils

(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

MP_L_EYE = [33, 160, 158, 133, 153, 144]
MP_R_EYE = [263, 387, 385, 362, 380, 373]

image_size = (320, 240)

runner_examples = """
Examples:
    python main.py server          # Start BlinkSense Server
    python main.py client          # Start BlinkSense Client
"""
