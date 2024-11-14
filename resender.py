import asyncio
import json
from datetime import datetime, timedelta
from telethon import TelegramClient
from subscription_utils import subscriptions

with open('data.json', 'r') as file:
    data = json.load(file)

api_id = data['app_id']
api_hash = data['api_hash']
phone_number = data['phone_number']

client = TelegramClient('session_name', api_id, api_hash)

async def message_fetcher():
    await client.start()
    while True:
        now = datetime.now().astimezone()
        time_limit = now - timedelta(seconds=10)
        for recipient_username, groups in subscriptions.items():
            for group_username, keywords in groups.items():
                group = await client.get_entity(group_username)

                async for message in client.iter_messages(group, limit=100):
                    if message.date > time_limit and message.text:
                        for keyword in keywords:
                            if keyword.lower() in message.text.lower():
                                await client.send_message(recipient_username, message.text)
                                print(f'Message sent to {recipient_username}: "{message.text}"')
                                break
            await asyncio.sleep(10)