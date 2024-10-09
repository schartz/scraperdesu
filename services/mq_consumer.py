import asyncio
import stomp
from icecream import ic
from config import AppConfig
from models import AMQMessage, ScrapeMessagePayload
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
        try:
            msg = AMQMessage(**json.loads(frame.body))
            if msg.message_type == 1:
                payload = ScrapeMessagePayload(**msg.payload)
                asyncio.run(scrap_the_website(payload.website_url))
        except Exception as e:
            ic("error", e)
        ic("ready for next message")

    def on_disconnected(self):
        self.conn.connect(config.ACTIVEMQ_USER, config.ACTIVEMQ_PASSCODE, wait=True)
        queues = [
            config.AQ_SCRAPE_QUEUE_SUB,
            config.AQ_RAG_INGEST_QUEUE_SUB,
        ]

        for q in queues:
            self.conn.subscribe(
                destination=q,
                id=q,
                ack="auto",
                headers={"persistent": "true", "routing_key": q},
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
        queues = [
            config.AQ_SCRAPE_QUEUE_SUB,
            config.AQ_RAG_INGEST_QUEUE_SUB,
        ]

        for q in queues:
            self.connection.subscribe(
                destination=q,
                id=q,
                ack="auto",
                headers={"persistent": "true", "routing_key": q},
            )
            print(config.AQ_SCRAPE_QUEUE_SUB)

    @staticmethod
    def get_message_broker() -> "MessageBroker":
        """Static method to fetch the current instance."""
        if not MessageBroker.__instance__:
            MessageBroker()
        return MessageBroker.__instance__  # pyright: ignore
