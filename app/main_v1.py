import asyncio
import logging
from resender import message_fetcher, message_sender
from synch_subscribers import synch_subscribers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger().setLevel(logging.INFO)

async def main():
    await asyncio.gather(message_fetcher(), synch_subscribers(), message_sender())

logging.info("Pull приложение запущено")
asyncio.run(main())