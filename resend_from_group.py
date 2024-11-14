import asyncio
from resender import message_fetcher
from server import run_flask

async def main():
    await asyncio.gather(run_flask(), message_fetcher())

if __name__ == '__main__':
    asyncio.run(main())
