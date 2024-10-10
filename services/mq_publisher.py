import json
import os
import time
import stomp
from loguru import logger

from config import AppConfig

config = AppConfig.get_config()


class ActiveMQPublisher(stomp.ConnectionListener):
    __instance__ = None
    activemq_conn = stomp.Connection([(config.ACTIVEMQ_HOST, config.ACTIVEMQ_PORT)])

    def __init__(self):
        """Constructor."""

        self.activemq_conn.set_listener("", self)
        if ActiveMQPublisher.__instance__ is None:
            ActiveMQPublisher.__instance__ = self
            self.default_queue = os.getenv("AQ_DEFAULT_QUEUE_PUB")
        else:
            raise Exception("You cannot create another ActiveMQPublisher class")

    def publish(self, msg: dict, routing_key: str = ""):
        message = json.dumps(msg, indent=2, ensure_ascii=False)

        self.ensure_connection()
        self.activemq_conn.send(
            body=message,
            destination=routing_key,
            headers={
                "persistent": "true",
                "routing_key": routing_key,
                "content_type": "application/json",
            },
        )

        logger.info(f"published message on---> {routing_key}")
        time.sleep(2)
        self.activemq_conn.disconnect()

    def ensure_connection(self):
        if not self.activemq_conn.is_connected():
            self.activemq_conn.connect(
                config.ACTIVEMQ_USER, config.ACTIVEMQ_PASSCODE, wait=True
            )

    @staticmethod
    def get_mq_connection() -> "ActiveMQPublisher":
        """Static method to fetch the current instance."""
        if not ActiveMQPublisher.__instance__:
            ActiveMQPublisher()
        return ActiveMQPublisher.__instance__
