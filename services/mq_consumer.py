import stomp

from config import AppConfig


config = AppConfig.get_config()


class Listener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame)

    def on_message(self, frame):
        print('received a message "%s"' % frame)

    def on_disconnected(self):
        self.conn.connect(config.ACTIVEMQ_USER, config.ACTIVEMQ_PASSCODE, wait=True)
        self.conn.subscribe(
            destination=f"/queue/{config.AQ_DEFAULT_QUEUE_SUB}",
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
            # connect_and_subscribe(self.connection)
        else:
            raise Exception("You cannot create another MessageBroker class")

    def subscribe_queue(self):
        self.connection.subscribe(
            destination=f"/queue/{config.AQ_DEFAULT_QUEUE_SUB}",
            id="1",
            ack="auto",
            headers={"persistent": "true", "routing_key": config.AQ_DEFAULT_QUEUE_SUB},
        )

    @staticmethod
    def get_message_broker() -> "MessageBroker":
        """Static method to fetch the current instance."""
        if not MessageBroker.__instance__:
            MessageBroker()
        return MessageBroker.__instance__  # pyright: ignore
