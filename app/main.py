import asyncio
import logging
from resender import message_fetcher
from synch_subscribers import synch_subscribers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger().setLevel(logging.INFO)

async def main():
    asyncio.create_task(message_fetcher())
    asyncio.create_task(synch_subscribers())

if __name__ == '__main__':
    logging.info("Приложение запущено")
    asyncio.run(main())