import json
import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_dir, 'credentials.json')

def get_credentials():
    try:
        with open(credentials_file_path, 'r') as file:
            data = json.load(file)

        logging.getLogger().debug(f"Developer mode")
        return data['api_id'], data['api_hash'], data['phone_number']

    except FileNotFoundError:
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone_number = os.getenv('PHONE_NUMBER')

        if not api_id or not api_hash or not phone_number:
            raise ValueError("Cant find value in file or in env")

        return api_id, api_hash, phone_number

def get_backend_credentials():
    try:
        with open(credentials_file_path, 'r') as file:
            data = json.load(file)

        logging.getLogger().debug(f"Developer mode")
        return data['backend_basic_auth_user'], data['backend_basic_auth_password']

    except FileNotFoundError:
        basic_auth_user = os.getenv('BACKEND_BASIC_AUTH_USER')
        basic_auth_password = os.getenv('BACKEND_BASIC_AUTH_PASSWORD')

        if not basic_auth_user or not basic_auth_password:
            raise ValueError("Cant find value in file or in env")

        return basic_auth_user, basic_auth_password

def get_backend_path():
    try:
        open(credentials_file_path, 'r')
        logging.getLogger().debug(f"Developer mode. Start backend on localhost:8080")
        return "http://127.0.0.1:8080/api/subscriptions"

    except FileNotFoundError:
        return "http://backend:8080/api/subscriptions"

def is_test_mode():
    try:
        open(credentials_file_path, 'r')
        return True
    except FileNotFoundError:
        return False