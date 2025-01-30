import os
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Enter api_id: "))
api_hash = input("Enter api_hash: ")
phone_number = input("Enter phone_number, format +7: ")

session_string = StringSession()

client = TelegramClient(session_string, api_id, api_hash)

client.start(phone_number)
session_str = client.session.save()
logging.getLogger().debug(f"Session string: {session_str}")

if not os.path.exists("../mounted"):
    os.makedirs("../mounted")

with open("../mounted/session.txt", "w", encoding="utf-8") as file:
    file.write(session_str)

logging.getLogger().debug("Session string saved in file")
