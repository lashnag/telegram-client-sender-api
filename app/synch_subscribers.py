from datetime import datetime

import requests
import asyncio
from subscription_utils import add_subscription, clear_subscriptions
from environments_loader import get_backend_path

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
                print(f"Sync get | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Subscriber: {item['subscriber']}, Subscription: {item['subscription']}, Keyword: {item['keyword']}")

        except requests.exceptions.HTTPError as http_err:
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Error occurred: {err}")
        except ValueError as json_err:
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"JSON decode error: {json_err}")

        await asyncio.sleep(100)