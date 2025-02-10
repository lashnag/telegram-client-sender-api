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

def get_backend_credentials():
    if is_prod_mode():
        basic_auth_user = os.getenv('BACKEND_BASIC_AUTH_USER')
        basic_auth_password = os.getenv('BACKEND_BASIC_AUTH_PASSWORD')

        if not basic_auth_user or not basic_auth_password:
            raise ValueError("Cant find value in file or in env")

        return basic_auth_user, basic_auth_password
    else:
        with open(credentials_file_path, 'r') as file:
            data = json.load(file)

        return data['backend_basic_auth_user'], data['backend_basic_auth_password']

def get_backend_path():
    if is_prod_mode():
        return "http://backend:8080/api/subscriptions"
    else:
        return "http://127.0.0.1:8080/api/subscriptions"

def get_lemmatizer_path():
    if is_prod_mode():
        return "http://lemmatizer:4355/lemmatize"
    else:
        return "http://127.0.0.1:4355/lemmatize"

def is_prod_mode():
    try:
        open(credentials_file_path, 'r')
        logging.getLogger().debug(f"Developer mode")
        return False
    except FileNotFoundError:
        return True