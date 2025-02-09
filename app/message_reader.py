import os
import logging
import pytesseract
from PIL import Image
from io import BytesIO
from telethon.errors.rpcerrorlist import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from environments_loader import get_credentials
from telethon.sessions import StringSession
from exceptions import InvalidGroupException

api_id, api_hash, phone_number = get_credentials()

current_dir = os.path.dirname(os.path.abspath(__file__))
session_file_path = os.path.join(current_dir, '../mounted/session.txt')

with open(session_file_path, "r", encoding="utf-8") as file:
    session_string = file.read()

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def fetch_messages(group_name, last_processed_message):
    await client.start(phone_number)
    messages = {}
    try:
        try:
            group = await client.get_entity(group_name)
        except (UsernameInvalidError, ValueError) as no_group:
            logging.getLogger().warning(f"No group error: {no_group}, {group_name}")
            raise InvalidGroupException(f"No group error: {no_group}, {group_name}")

        try:
            await client.start(phone_number)
            await client(JoinChannelRequest(group))
        except Exception as e:
            logging.getLogger().warning(f"An error occurred when trying to join the group: {group_name} {e}")
            raise InvalidGroupException(f"An error occurred when trying to join the group: {group_name} {e}")

        logging.getLogger().info(f"Get messages for subscription: {group_name}")
        async for message in client.iter_messages(group, limit=10, min_id=last_processed_message):
            messages[message.id] = {}
            if message.text:
                messages[message.id]["text"] = message.text
            if message.media:
                if hasattr(message.media, 'photo'):
                    try:
                        file_buffer = BytesIO()
                        await message.client.download_media(message, file=file_buffer)
                        file_buffer.seek(0)
                        image = Image.open(file_buffer)
                        extracted_text_en = pytesseract.image_to_string(image, lang='eng')
                        extracted_text_ru = pytesseract.image_to_string(image, lang='rus')
                        messages[message.id]["image_text_ru"] = extracted_text_ru
                        messages[message.id]["image_text_en"] = extracted_text_en
                    except Exception as e:
                        logging.getLogger().error(f"Error downloading message ID {message.id}: {e}")

        return messages

    except InvalidGroupException:
        raise
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise