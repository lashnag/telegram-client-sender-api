import contextvars
import logging
import json
import os
import sys
import traceback
from logstash_async.handler import AsynchronousLogstashHandler

request_headers = contextvars.ContextVar('request_headers')

def is_remote_logger():
    env_value = os.getenv('REMOTE_LOGGER', '').lower()
    if env_value == 'true':
        logging.getLogger().info("Remote logger")
        return True
    else:
        logging.getLogger().info("Local logger")
        return False

def init_logger():
    main_handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_remote_logger() else logging.StreamHandler(sys.stdout)
    main_handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=logging.INFO,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [main_handler]
    )

    telegram_messages_logger = logging.getLogger("telegram_messages_logger")
    telegram_messages_logger.setLevel(logging.INFO)
    telegram_messages_handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_remote_logger() else logging.StreamHandler()
    telegram_messages_handler.setFormatter(TelegramMessagesJsonFormatter())
    telegram_messages_logger.addHandler(telegram_messages_handler)
    telegram_messages_logger.propagate = False

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'application': 'sender-api',
            'level': record.levelname,
            'message': record.getMessage(),
            'logger_name': record.filename,
        }
        if record.exc_info:
            log_obj['exception'] = ''.join(traceback.format_exception(*record.exc_info))

        headers = request_headers.get(None)
        if isinstance(headers, dict):
            for key, value in headers.items():
                if key.startswith('custom-'):
                    log_obj[key.removeprefix('custom-')] = value

        return json.dumps(log_obj)

class TelegramMessagesJsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'application': 'telegram-messages',
            'level': record.levelname,
            'message': record.getMessage(),
            'logger_name': record.filename,
        }

        if hasattr(record, 'extra_fields') and isinstance(record.extra_fields, dict):
            for key, value in record.extra_fields.items():
                if value is not None:
                    log_obj[key] = value

        return json.dumps(log_obj)