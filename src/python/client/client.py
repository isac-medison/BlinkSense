"""
Main client orchestrator module
"""
import cv2
import socket
import base64
from logging import getLogger

from src.python.config.config import get_config
from src.python.constants import image_size

class Client:
    """
    Main Client Class
    Responsible for connecting to BlinkSense and sending video frames
    """

    def __init__(self):
        self.config = get_config()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.video_capture = cv2.VideoCapture(0)
        self.logger = getLogger('client')

    def __enter__(self):
        self.logger.info('Client started')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self.video_capture.release()
        self.socket.close()
        self.logger.info("Client resources released.")

    def send_frame(self):
        ret, frame = self.video_capture.read()

        if not ret:
            return

        frame = cv2.resize(frame, image_size)
        encoded, buffer = cv2.imencode('.jpg', frame)
        data = base64.b64encode(buffer)

        if len(data) > self.config.buffer_size:
            self.logger.info("Frame too large, skipping.")
            return

        self.socket.sendto(data, (self.config.server_ip, self.config.server_port))
