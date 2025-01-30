import json
import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')
logger = logging.getLogger('environment_loader')

def load_credentials():
    try:
        with open(credentials_file_path, 'r') as file:
            data = json.load(file)

        logger.debug(f"Developer mode")
        return data['api_id'], data['api_hash'], data['phone_number']

    except FileNotFoundError:
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone_number = os.getenv('PHONE_NUMBER')

        if not api_id or not api_hash or not phone_number:
            raise ValueError("Не удалось найти необходимые данные ни в файле, ни в переменных окружения")

        return api_id, api_hash, phone_number

def get_backend_path():
    try:
        open(credentials_file_path, 'r')
        logger.debug(f"Developer mode. Start backend on localhost:8080")
        return "http://127.0.0.1:8080/api/subscriptions"

    except FileNotFoundError:
        return "http://backend:8080/api/subscriptions"

def is_test_mode():
    try:
        open(credentials_file_path, 'r')
        return True
    except FileNotFoundError:
        return False