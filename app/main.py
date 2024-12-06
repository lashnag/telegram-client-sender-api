import asyncio
import logging
from resender import message_fetcher
from synch_subscribers import synch_subscribers

async def main():
    await asyncio.gather(message_fetcher(), synch_subscribers())

if __name__ == '__main__':
    asyncio.run(main())
    logging.info("Приложение запущено")