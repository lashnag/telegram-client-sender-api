import base64
import os
import logging
from io import BytesIO
from telethon import TelegramClient
from environments_loader import get_credentials
from telethon.sessions import StringSession

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
        group = await client.get_entity(f"https://t.me/{group_name}")
        logging.getLogger().info(f"Get messages for subscription: {group_name}")
        async for message in client.iter_messages(group, limit=10, min_id=last_processed_message):
            messages[message.id] = {}
            if message.text:
                logging.getLogger("telegram_messages_logger").info(message.text, extra={
                    'extra_fields': {
                        'group_name': group_name,
                        'message_id': message.id,
                        'user': getattr(message.sender, 'username', None)
                    }
                })
                messages[message.id]["text"] = message.text
            if message.media:
                if hasattr(message.media, 'photo'):
                    try:
                        file_buffer = BytesIO()
                        await message.client.download_media(message, file=file_buffer)
                        file_buffer.seek(0)
                        encoded_string = base64.b64encode(file_buffer.read()).decode('utf-8')
                        messages[message.id]["image"] = encoded_string
                    except Exception as e:
                        logging.getLogger().error(f"Error downloading message ID {message.id}: {e}")

        return messages

    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise