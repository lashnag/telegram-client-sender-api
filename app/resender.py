import asyncio
import re
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime, timedelta
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from subscription_utils import subscriptions, exception_subscriptions
from environments_loader import load_credentials
from telethon.sessions import StringSession

api_id, api_hash, phone_number = load_credentials()

with open("mounted/session.txt", "r", encoding="utf-8") as file:
    session_string = file.read()

client = TelegramClient(StringSession(session_string), api_id, api_hash)
russian_stemmer = SnowballStemmer("russian")
processed_message_ids = set()

async def message_fetcher():
    await client.start(phone_number)
    while True:
        try:
            for recipient_username, groups in subscriptions.items():
                for group_username, keywords in groups.items():
                    if group_username in exception_subscriptions:
                        continue

                    try:
                        group = await client.get_entity(group_username)
                    except UsernameInvalidError as no_group:
                        exception_subscriptions.add(no_group.request.username)
                        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"No group error: {no_group}, added to ignore list")
                        continue

                    await join_public_group(group)
                    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Check messages for subscriber: {recipient_username}, subscription: {group_username}, keyword: {keywords}")
                    async for message in client.iter_messages(group, limit=100):
                        if message.text and message.id not in processed_message_ids:
                            processed_message_ids.add(message.id)
                            for keyword in keywords:
                                words_in_message = re.findall(r'\b\w+\b', message.text.lower())
                                words_in_keyword = re.findall(r'\b\w+\b', keyword.lower())
                                stems_in_message = [russian_stemmer.stem(token) for token in words_in_message if token.isalpha()]
                                stems_in_keyword = [russian_stemmer.stem(token) for token in words_in_keyword if token.isalpha()]
                                if all(stem in stems_in_message for stem in stems_in_keyword):
                                    await client.send_message(recipient_username, message.text)
                                    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                                    print(f'Message sent to {recipient_username}: "{message.text}"')
                                    break

        except Exception as error:
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Common error: {error}")

        await asyncio.sleep(10)


async def join_public_group(group_username):
    await client.start(phone_number)

    try:
        await client(JoinChannelRequest(group_username))
    except Exception as e:
        exception_subscriptions.add(group_username)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"An error occurred when trying to join the group: {group_username} {e}, added to ignore list")