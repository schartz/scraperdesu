import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


class AppConfig:
    __instance__ = None

    def __init__(self):
        """Constructor."""
        if AppConfig.__instance__ is None:
            AppConfig.__instance__ = self

            env_path = Path(".") / ".env"
            load_dotenv(dotenv_path=env_path)

            self.APP_PROFILE = os.getenv("APP_PROFILE") == "False"
            self.EXCLUDED_PATH = os.getenv("EXCLUDED_PATH", "/tmp")
            self.ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "localhost")
            self.ACTIVEMQ_PORT = int(os.getenv("ACTIVEMQ_PORT", "61613"))
            self.ACTIVEMQ_USER = os.getenv("ACTIVEMQ_USER", "artemis")
            self.ACTIVEMQ_PASSCODE = os.getenv("ACTIVEMQ_PASSCODE", "artemis")
            self.AQ_DEFAULT_QUEUE_SUB = os.getenv(
                "AQ_DEFAULT_QUEUE_CONSUMER", "sub_default_queue"
            )
            self.AQ_DEFAULT_QUEUE_PUB = os.getenv(
                "AQ_DEFAULT_QUEUE", "pub_default_queue"
            )

        else:
            raise Exception("You cannot create another AppConfig class")

    @staticmethod
    def get_config() -> "AppConfig":
        """Static method to fetch the current instance."""
        if not AppConfig.__instance__:
            AppConfig()
        return AppConfig.__instance__  # pyright: ignore
