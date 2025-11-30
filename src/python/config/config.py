"""
Configuration file for BlinkSense project
Manages all environment variables and application settings
"""


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ Application settings loaded from environment variables. """

    # General
    buffer_size:int = 65507
    fps:int = 10

    # Server
    server_ip:str = "127.0.0.1"
    server_port:int = 8000

    #Notification
    ear_trash:float = 0.42

    ear_delta:float = 0.1
    contrast:int = 5
    client_name:str = "Client #1"
    blink_time_window:int = 5
    log_file:str = "blinksense.log"

    alerts_enabled:bool = False
    smtp_server:str= "smtp.gmail.com"
    smtp_port:int= 587
    smtp_user:str= "admin@example.com"
    smtp_password:str= "password_here"
    recipient_email:str= "admin@example.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

def get_config():
    return settings

