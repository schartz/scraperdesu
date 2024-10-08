import asyncio
from icecream import ic
import traceback

from services.mq_consumer import MessageBroker
from services.scrapper.scrap import scrap_the_website


async def main(event_loop):
    conn = MessageBroker.get_message_broker()
    conn.subscribe_queue()
    return conn
    # await scrap_the_website(sys.argv[1])


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.run(main(loop))
    try:
        loop.run_forever()
    except Exception as e:
        traceback.print_exc()
        ic(e)
