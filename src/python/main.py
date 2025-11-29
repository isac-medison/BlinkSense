"""
Main entry point of BlinkSense project.
Provides command-line interface.
"""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import logging
from logging.handlers import RotatingFileHandler
import time
from config.config import get_config
import constants
from client.client import Client
from server.server import Server

class BlinkSenseApp():
    def __init__(self):
        self.config = get_config()
        self.logger = logging.getLogger('BlinkSense')
        self.parser = argparse.ArgumentParser(description='BlinkSense Sense',
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog=constants.runner_examples,)
        self.parser.add_argument('command', choices=["server", "client"], help="Command to execute")
        self.parser.add_argument('ip', nargs="?", help="IP address to connect to")
        self.parser.add_argument('--debug', action="store_true", help="Enable debug mode")
        self.args = self.parser.parse_args()

    def start_client(self):
        """
        Start the BlinkSense client.
        """
        if self.config.fps <= 0:
            raise ValueError("FPS should be greater than 0")
        with Client() as client:
            while True:
                client.send_frame()
                time.sleep(1 / self.config.fps)


    def start_blink_server(self):
        """
        Start the BlinkSense server.
        """
        with Server() as server:
            server.start()
        return 0


    def run(self):
        """
        Entry point with command-line interface argument parsing.
        """
        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)

        try:
            if self.args.command == "client":
                return self.start_client()
            elif self.args.command == "server":
                return self.start_blink_server()

            self.logger.error("Unexpected command")
            return 0

        except KeyboardInterrupt:
            self.logger.info("Interrupted by user.")
            return 0
        except Exception as e:
            self.logger.error("Unexpected error %s",str(e))
            return 1


if __name__ == "__main__":
    app = BlinkSenseApp()
    log_file = app.config.log_file
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    sys.exit(app.run())
