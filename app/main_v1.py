import asyncio
import logging
from resender import message_fetcher, message_sender
from synch_subscribers import synch_subscribers
from logger import init_logger

init_logger()
logging.getLogger("main_v1").info("Pull приложение запущено")

async def main():
    await asyncio.gather(message_fetcher(), synch_subscribers(), message_sender())

asyncio.run(main())