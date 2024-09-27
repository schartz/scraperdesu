import asyncio
import sys

from services.mq_consumer import MessageBroker
from services.scrapper.scrap import scrap_the_website


async def main():
    conn = MessageBroker.get_message_broker()
    conn.subscribe_queue()
    await scrap_the_website(sys.argv[1])


if __name__ == "__main__":
    asyncio.run(main())
