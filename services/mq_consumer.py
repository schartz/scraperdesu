import asyncio
import stomp
from icecream import ic
from config import AppConfig
from services.scrapper.scrap import scrap_the_website
import json

config = AppConfig.get_config()


class Listener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        # AMQ229014 is the error code for disconnection after 60 seconds timeout.
        # if we encounter this error, ignore it
        if not frame.headers["message"].startswith("AMQ229014"):
            print('received an error "%s"' % frame)

    def on_message(self, frame):
        print('received a message "%s"' % frame)
        msg = json.loads(frame.body)
        asyncio.run(scrap_the_website(msg["payload"]["website_url"]))

    def on_disconnected(self):
        self.conn.connect(config.ACTIVEMQ_USER, config.ACTIVEMQ_PASSCODE, wait=True)
        self.conn.subscribe(
            destination=config.AQ_DEFAULT_QUEUE_SUB,
            id="1",
            ack="auto",
            headers={"persistent": "true", "routing_key": config.AQ_DEFAULT_QUEUE_SUB},
        )


class MessageBroker:
    __instance__ = None

    def __init__(self):
        """Constructor."""
        print("Message Broker Init")
        if MessageBroker.__instance__ is None:
            MessageBroker.__instance__ = self
            self.connection = stomp.Connection(
                [(config.ACTIVEMQ_HOST, config.ACTIVEMQ_PORT)]
            )
            self.connection.set_listener("", Listener(self.connection))
            self.connection.connect(
                config.ACTIVEMQ_USER, config.ACTIVEMQ_PASSCODE, wait=True
            )
        else:
            raise Exception("You cannot create another MessageBroker class")

    def subscribe_queue(self):
        self.connection.subscribe(
            destination=config.AQ_DEFAULT_QUEUE_SUB,
            id="1",
            ack="auto",
            headers={"persistent": "true", "routing_key": config.AQ_DEFAULT_QUEUE_SUB},
        )
        print(config.AQ_DEFAULT_QUEUE_SUB)

    @staticmethod
    def get_message_broker() -> "MessageBroker":
        """Static method to fetch the current instance."""
        if not MessageBroker.__instance__:
            MessageBroker()
        return MessageBroker.__instance__  # pyright: ignore
