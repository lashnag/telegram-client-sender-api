import requests
import asyncio
import logging
from datetime import datetime
from subscription_utils import add_subscription, clear_subscriptions
from environments_loader import get_backend_path

async def synch_subscribers():
    url = get_backend_path()

    while True:
        logging.getLogger().info(f"Log synch message")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            clear_subscriptions()
            for item in data:
                add_subscription(item['subscriber'], item['subscription'], item['keyword'])
                logging.getLogger().info(f"Sync get | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logging.getLogger().info(f"Subscriber: {item['subscriber']}, Subscription: {item['subscription']}, Keyword: {item['keyword']}")

        except requests.exceptions.HTTPError as http_err:
            logging.getLogger().error(f"HTTP error occurred: {http_err}", exc_info=True)
        except requests.exceptions.RequestException as err:
            logging.getLogger().error(f"Error occurred: {err}", exc_info=True)
        except ValueError as json_err:
            logging.getLogger().error(f"JSON decode error: {json_err}", exc_info=True)

        await asyncio.sleep(1)