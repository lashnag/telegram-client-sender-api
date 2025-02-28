import contextvars
import logging
import json
import traceback
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_prod_mode

request_headers = contextvars.ContextVar('request_headers')

def init_logger():
    main_handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_prod_mode() else logging.StreamHandler()
    main_handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=logging.INFO if is_prod_mode() else logging.DEBUG,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [main_handler]
    )

    telegram_messages_logger = logging.getLogger("telegram_messages_logger")
    telegram_messages_logger.setLevel(logging.INFO if is_prod_mode() else logging.DEBUG)
    telegram_messages_handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_prod_mode() else logging.StreamHandler()
    telegram_messages_handler.setFormatter(TelegramMessagesJsonFormatter())
    telegram_messages_logger.addHandler(telegram_messages_handler)
    telegram_messages_logger.propagate = False

    logging.getLogger().info(f"Prod mode: {is_prod_mode()}")

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