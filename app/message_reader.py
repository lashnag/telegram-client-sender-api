import os
import logging
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from environments_loader import load_credentials
from telethon.sessions import StringSession
from exceptions import InvalidGroupException

api_id, api_hash, phone_number = load_credentials()

current_dir = os.path.dirname(os.path.abspath(__file__))
session_file_path = os.path.join(current_dir, '../mounted/session.txt')
with open(session_file_path, "r", encoding="utf-8") as file:
    session_string = file.read()

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def fetch_messages(group_name, last_processed_message):
    await client.start(phone_number)
    messages = []
    last_message_id = None
    try:
        try:
            group = await client.get_entity(group_name)
        except UsernameInvalidError as no_group:
            logging.warn(f"No group error: {no_group}, {group_name}")
            raise InvalidGroupException

        try:
            await client.start(phone_number)
            await client(JoinChannelRequest(group))
        except Exception as e:
            logging.warn(f"An error occurred when trying to join the group: {group.username} {e}")
            raise InvalidGroupException

        logging.info(f"Get messages for subscription: {group_name}")
        async for message in client.iter_messages(group, limit=10, min_id=last_processed_message):
            if message.text:
                messages.append(message.text)
                last_message_id = message.id

        return messages, last_message_id

    except InvalidGroupException:
        raise
    except Exception as error:
        logging.error(f"Common error: {error}", exc_info=True)
        raise