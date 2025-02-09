import requests
import asyncio
import logging
from requests.auth import HTTPBasicAuth
from datetime import datetime
from subscription_utils import add_subscription, clear_subscriptions
from environments_loader import get_backend_path, get_backend_credentials

async def synch_subscribers():
    url = get_backend_path()
    backend_basic_auth_user, backend_basic_auth_password = get_backend_credentials()

    while True:
        try:
            response = requests.get(url, auth=HTTPBasicAuth(backend_basic_auth_user, backend_basic_auth_password))
            response.raise_for_status()
            data = response.json()
            logging.getLogger().info(f"Sync get | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            clear_subscriptions()
            for item in data:
                add_subscription(item['subscriber'], item['subscription'], item['keyword'])
                logging.getLogger().debug(f"Subscriber: {item['subscriber']}, Subscription: {item['subscription']}, Keyword: {item['keyword']}")

        except requests.exceptions.HTTPError as http_err:
            logging.getLogger().error(f"HTTP error occurred: {http_err}", exc_info=True)
        except requests.exceptions.RequestException as err:
            logging.getLogger().error(f"Error occurred: {err}", exc_info=True)
        except ValueError as json_err:
            logging.getLogger().error(f"JSON decode error: {json_err}", exc_info=True)

        await asyncio.sleep(100)