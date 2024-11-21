from telethon import TelegramClient
from environments_loader import load_credentials
from telethon.sessions import StringSession

api_id, api_hash, phone_number = load_credentials()

session_string = StringSession()

client = TelegramClient(session_string, api_id, api_hash)

client.start()
session_str = client.session.save()
print("Строка сессии:", session_str)

with open("../mounted/session.txt", "w", encoding="utf-8") as file:
    file.write(session_str)

print("Строка сессии успешно сохранена в файл!")
