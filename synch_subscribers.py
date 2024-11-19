import requests
import asyncio
from subscription_utils import add_subscription, clear_subscriptions

async def synch_subscribers():
    url = 'http://127.0.0.1:8080/api/subscriptions'

    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            clear_subscriptions()
            for item in data:
                add_subscription(item['subscriber'], item['subscription'], item['keyword'])
                print(f"Sync get | Subscriber: {item['subscriber']}, Subscription: {item['subscription']}, Keyword: {item['keyword']}")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")

        await asyncio.sleep(100)