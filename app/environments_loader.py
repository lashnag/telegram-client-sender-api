import json
import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')

def get_credentials():
    if is_prod_mode():
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone_number = os.getenv('PHONE_NUMBER')

        if not api_id or not api_hash or not phone_number:
            raise ValueError("Cant find value in file or in env")

        return api_id, api_hash, phone_number
    else:
        with open(credentials_file_path, 'r') as file:
            data = json.load(file)
        return data['api_id'], data['api_hash'], data['phone_number']

def is_prod_mode():
    if os.getenv('PROD_MODE') is not None:
        logging.getLogger().info("Production mode")
        return True
    else:
        logging.getLogger().info("Developer mode")
        return False