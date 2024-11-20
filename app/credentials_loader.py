import json
import os

def load_credentials():
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)

        return data['api_id'], data['api_hash'], data['phone_number']

    except FileNotFoundError:
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone_number = os.getenv('PHONE_NUMBER')

        if not api_id or not api_hash or not phone_number:
            raise ValueError("Не удалось найти необходимые данные ни в файле, ни в переменных окружения")

        return api_id, api_hash, phone_number