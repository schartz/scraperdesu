import json
import os
import time
from typing import Union
import stomp


class ActiveMQPublisher(stomp.ConnectionListener):
    __instance__ = None
    activemq_conn = stomp.Connection(
        host_and_ports=
        [(os.getenv("ACTIVEMQ_HOST", "127.0.0.1"),
          int(os.getenv("ACTIVEMQ_PORT", 61613)))]
    )

    def __init__(self):
        """Constructor."""

        self.activemq_conn.set_listener('', self)
        if ActiveMQPublisher.__instance__ is None:
            ActiveMQPublisher.__instance__ = self
            self.default_queue = os.getenv("AQ_DEFAULT_QUEUE_PUB")
        else:
            raise Exception("You cannot create another ActiveMQPublisher class")

    def publish(self, msg: dict, routing_key: str = ""):
        message = json.dumps(msg, indent=2, ensure_ascii=False)

        self.ensure_connection()
        self.activemq_conn.send(body=message,
                                destination=f'/queue/{routing_key}',
                                headers={'persistent': 'true',
                                         'routing_key': routing_key,
                                         'content_type': 'application/json'})

        print(f"published message on---> {routing_key}")
        time.sleep(2)
        self.activemq_conn.disconnect()

    def ensure_connection(self):
        if not self.activemq_conn.is_connected():
            self.activemq_conn.connect(os.getenv("ACTIVEMQ_USER", "admin"),
                                       os.getenv("ACTIVEMQ_PASSCODE", "admin"),
                                       wait=True)

    @staticmethod
    def get_mq_connection() -> "ActiveMQPublisher":
        """Static method to fetch the current instance."""
        if not ActiveMQPublisher.__instance__:
            ActiveMQPublisher()
        return ActiveMQPublisher.__instance__
