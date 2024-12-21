import os
import asyncio
import re
import logging
from nltk.stem.snowball import SnowballStemmer
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from subscription_utils import subscriptions, exception_subscriptions, add_processed_message, is_message_processed
from environments_loader import load_credentials
from telethon.sessions import StringSession

api_id, api_hash, phone_number = load_credentials()

current_dir = os.path.dirname(os.path.abspath(__file__))
session_file_path = os.path.join(current_dir, '../mounted/session.txt')
with open(session_file_path, "r", encoding="utf-8") as file:
    session_string = file.read()

client = TelegramClient(StringSession(session_string), api_id, api_hash)
russian_stemmer = SnowballStemmer("russian")
message_queue = asyncio.Queue()

async def message_fetcher():
    await client.start(phone_number)
    while True:
        try:
            for group_name, subscribers_keywords in subscriptions.items():
                if group_name in exception_subscriptions:
                    continue

                try:
                    group = await client.get_entity(group_name)
                except UsernameInvalidError as no_group:
                    exception_subscriptions.add(group_name)
                    logging.warn(f"No group error: {no_group}, added to ignore list {group_name}")
                    continue

                await join_public_group(group)
                logging.info(f"Check messages for subscription: {group_name}")
                async for message in client.iter_messages(group, limit=10):
                    if message.text:
                        for subscriber, keywords in subscribers_keywords.items():
                            logging.info(f"Check messages for subscriber: {subscriber}, keywords: {keywords}")
                            if is_message_processed(subscriber, group_name, message.id):
                                continue

                            add_processed_message(subscriber, group_name, message.id)
                            for keyword in keywords:
                                words_in_message = re.findall(r'\b\w+\b', message.text.lower())
                                words_in_keyword = re.findall(r'\b\w+\b', keyword.lower())
                                stems_in_message = [russian_stemmer.stem(token) for token in words_in_message if token.isalpha()]
                                stems_in_keyword = [russian_stemmer.stem(token) for token in words_in_keyword if token.isalpha()]
                                if all(stem in stems_in_message for stem in stems_in_keyword):
                                    await message_queue.put((subscriber, message.text, message.id, group_name))
                                    break

        except Exception as error:
            logging.error(f"Common error: {error}", exc_info=True)

        await asyncio.sleep(30)


async def join_public_group(group):
    await client.start(phone_number)

    try:
        await client(JoinChannelRequest(group))
    except Exception as e:
        exception_subscriptions.add(group.username)
        logging.warn(f"An error occurred when trying to join the group: {group.username} {e}, added to ignore list")

async def message_sender():
    while True:
        subscriber, text, message_id, group_name = await message_queue.get()
        message_link = f"https://t.me/{group_name}/{message_id}"
        full_text = (
            f"{text}\n\n"
            f"Сообщение переслано из группы: @{group_name}\n"
            f"[Перейти к сообщению]({message_link})"
        )
        try:
            await client.send_message(subscriber, full_text, link_preview=False)
            logging.info(f'Message sent to {subscriber}: "{text}"')
        except Exception as e:
            logging.error(f"Failed to send message to {subscriber}: {e}")
        await asyncio.sleep(30)