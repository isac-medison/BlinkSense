"""
Main server orchestrator module
"""
from logging import getLogger
from src.python.config.config import get_config
import socket
import base64
import cv2
import numpy as np
from typing import Tuple

from src.python.preprocessor.preprocessor import Preprocessor
from src.python.detector.dnn_m import Detector
from src.python.interpreter.interpreter import Interpreter
from src.python.notifier.notifier import Notifier
from src.python.utils import put_custom_text, is_blink


class Server:
    """
    Main Server Class
    Responsible for listening Client and processing video frames
    """

    def __init__(self):
        self.config = get_config()
        self.running = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.prepr = Preprocessor()
        self.detector = Detector()
        self.notifier = Notifier()
        self.inter = Interpreter(self.notifier)
        self.logger = getLogger("server")
        self.prev_ear = 0

    def __enter__(self):
        self.socket.bind((self.config.server_ip, self.config.server_port))
        self.logger.info(
            f"Server listening on {self.config.server_ip}:{self.config.server_port}"
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
        cv2.destroyAllWindows()
        self.logger.info("Resources released.")

    def start(self):
        try:
            self.running = True
            while self.running:
                data, addr = self.socket.recvfrom(self.config.buffer_size)
                self.handle_frame(data, addr)

                if cv2.waitKey(1) & 0xFF == 27:  # ESC
                    self.running = False

        except KeyboardInterrupt:
            self.logger.info("Server shutting down")

    def handle_frame(self, data: bytes, addr: Tuple[str, int]):
        """
        Server execution flow
        """
        try:
            frame_data = base64.b64decode(data)
            np_data = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            frame = self.prepr.preprocess(frame)
            frame = self.detector.detect(frame)
            self.inter.clear_old_blinks()

            if is_blink(self.prev_ear, self.detector.ear):
                self.inter.blink()
            self.prev_ear = self.detector.ear

            self.inter.check_event()

            put_custom_text(frame, self.detector.ear, len(self.inter.blink_times))
            cv2.imshow(f"{self.config.client_name}", frame)

        except Exception as e:
            self.logger.error(f"Decoding error from {addr}: {e}", exc_info=True)
