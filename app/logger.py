import contextvars
import logging
import json
import traceback
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_prod_mode

request_headers = contextvars.ContextVar('request_headers')

def init_logger():
    handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    ) if is_prod_mode() else logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=logging.INFO if is_prod_mode() else logging.DEBUG,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [handler]
    )

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