import asyncio
import traceback
import sys

from services.scrapper.scrap import scrap_the_website


async def main():
    await scrap_the_website(sys.argv[1])


if __name__ == "__main__":
    asyncio.run(main())
