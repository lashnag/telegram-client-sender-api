import requests
import asyncio
import logging
from datetime import datetime
from subscription_utils import add_subscription, clear_subscriptions
from environments_loader import get_backend_path

logger = logging.getLogger('synch_subscribers')

async def synch_subscribers():
    url = get_backend_path()

    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            clear_subscriptions()
            for item in data:
                add_subscription(item['subscriber'], item['subscription'], item['keyword'])
                logger.info(f"Sync get | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"Subscriber: {item['subscriber']}, Subscription: {item['subscription']}, Keyword: {item['keyword']}")

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}", exc_info=True)
        except requests.exceptions.RequestException as err:
            logger.error(f"Error occurred: {err}", exc_info=True)
        except ValueError as json_err:
            logger.error(f"JSON decode error: {json_err}", exc_info=True)

        await asyncio.sleep(100)