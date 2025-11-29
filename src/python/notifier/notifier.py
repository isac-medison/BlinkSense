import logging
import smtplib
from src.python.config.config import get_config


class Notifier:
    def __init__(self):
        self.config = get_config()
        self.logger = logging.getLogger("Interpreter")

    def notify(self):
        subject = f"{self.config.client_name} is notifying high blink rate"
        body = "A high blink rate event has been detected by the BlinkSense system."
        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
            server.starttls()
            server.login(self.config.smtp_user, self.config.smtp_password)
            server.sendmail(self.config.smtp_user, self.config.recipient_email, message)
