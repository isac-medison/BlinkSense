import logging
from src.python.config.config import get_config
from src.python.utils import get_time


class Interpreter:
    def __init__(self, notifier):
        self.config = get_config()
        self.logger = logging.getLogger("interpreter")
        self.blink_times = []
        self.notifier = notifier
        self.last_cleanup = get_time()

    def clear_old_blinks(self):
        current_time = get_time()

        if current_time - self.last_cleanup >= 1:
            self.blink_times = [t for t in self.blink_times if current_time - t <= self.config.blink_time_window]
            self.last_cleanup = get_time()

    def blink(self):
        current_time = get_time()
        self.blink_times.append(current_time)
        self.check_event()

    def check_event(self):
        if len(self.blink_times) >= 5:
            self.notify()

    def notify(self):
        self.blink_times.clear()
        if self.config.alerts_enabled:
            self.logger.info("Notifying high blink rate")
            self.notifier.notify()

