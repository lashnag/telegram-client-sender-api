import os
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Введите api_id: "))
api_hash = input("Введите api_hash: ")
phone_number = input("Введите phone_number в формате +7: ")

session_string = StringSession()

client = TelegramClient(session_string, api_id, api_hash)

client.start(phone_number)
session_str = client.session.save()
logging.debug(f"Строка сессии: {session_str}")

if not os.path.exists("../mounted"):
    os.makedirs("../mounted")

with open("../mounted/session.txt", "w", encoding="utf-8") as file:
    file.write(session_str)

logging.debug("Строка сессии успешно сохранена в файл!")
