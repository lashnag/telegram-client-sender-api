import os
import asyncio
import re
import logging
import markdown
import requests
from bs4 import BeautifulSoup
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from exceptions import LemmatizationError
from subscription_utils import subscriptions, exception_subscriptions, add_processed_message, is_message_processed
from environments_loader import get_credentials, get_lemmatizer_path
from telethon.sessions import StringSession

api_id, api_hash, phone_number = get_credentials()

current_dir = os.path.dirname(os.path.abspath(__file__))
session_file_path = os.path.join(current_dir, '../mounted/session.txt')
with open(session_file_path, "r", encoding="utf-8") as file:
    session_string = file.read()

client = TelegramClient(StringSession(session_string), api_id, api_hash)
message_queue = asyncio.Queue()
lemmatizer = get_lemmatizer_path()

async def message_fetcher():
    await client.start(phone_number)
    await asyncio.sleep(100)  # Задержка на время пока не запустилось Java приложение
    while True:
        try:
            for group_name, subscribers_keywords in subscriptions.items():
                if group_name in exception_subscriptions:
                    continue

                try:
                    group = await client.get_entity(group_name)
                except UsernameInvalidError as no_group:
                    exception_subscriptions.add(group_name)
                    logging.getLogger().warning(f"No group error: {no_group}, added to ignore list {group_name}")
                    continue

                await join_public_group(group, group_name)
                logging.getLogger().info(f"Check messages for group_name: {group_name}")
                async for message in client.iter_messages(group, limit=10):
                    if message.text:
                        for subscriber, keywords in subscribers_keywords.items():
                            logging.getLogger().debug(f"Check messages for subscriber: {subscriber}, keywords: {keywords}, group name: {group_name}")
                            if is_message_processed(subscriber, group_name, message.id):
                                continue

                            add_processed_message(subscriber, group_name, message.id)
                            for keyword in keywords:
                                words_in_message = re.findall(r'\b\w+\b', md_to_text(message.text.lower()))
                                words_in_keyword = re.findall(r'\b\w+\b', keyword.lower())
                                lemmas_in_message = [lemmatize(token) for token in words_in_message if token.isalpha()]
                                lemmas_in_keyword = [lemmatize(token) for token in words_in_keyword if token.isalpha()]
                                if all(stem in lemmas_in_message for stem in lemmas_in_keyword):
                                    await message_queue.put((subscriber, message.text, message.id, group_name))
                                    break

        except Exception as error:
            logging.getLogger().error(f"Common error: {error}", exc_info=True)

        await asyncio.sleep(30)


async def join_public_group(group, group_name):
    await client.start(phone_number)

    try:
        await client(JoinChannelRequest(group))
    except Exception as e:
        exception_subscriptions.add(group_name)
        logging.getLogger().warning(f"An error occurred when trying to join the group: {group_name} {e}, added to ignore list")

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
            logging.getLogger().info(f'Message sent to {subscriber}: "{text}"')
        except Exception as e:
            logging.getLogger().error(f"Failed to send message to {subscriber}: {e}")
        await asyncio.sleep(30)

def md_to_text(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()


def lemmatize(token):
    payload = {"word": token}
    response = requests.post(lemmatizer, json=payload)

    if response.status_code != 200:
        raise LemmatizationError(f"Error: {response.status_code}")
    json_response = response.json()
    if "lemmatized" not in json_response:
        raise LemmatizationError("Key 'lemmatized' not found in response.")

    return response.json().get("lemmatized")