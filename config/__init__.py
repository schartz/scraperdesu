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

            self.APP_PROFILE = os.getenv("APP_PROFILE") == "True"
            self.EXCLUDED_PATH = os.getenv("EXCLUDED_PATH", "/tmp")

        else:
            raise Exception("You cannot create another AppConfig class")

    @staticmethod
    def get_config() -> "AppConfig":
        """Static method to fetch the current instance."""
        if not AppConfig.__instance__:
            AppConfig()
        return AppConfig.__instance__
