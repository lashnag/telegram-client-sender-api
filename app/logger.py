import logging
import json
import traceback
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_test_mode

def init_logger():
    handler = logging.StreamHandler() if is_test_mode() else AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None,
    )
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=logging.DEBUG if is_test_mode() else logging.INFO,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [handler]
    )

    logging.getLogger().info(f"Test mode: {is_test_mode()}")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'application': 'sender-api',
            'level': record.levelname,
            'message': record.getMessage(),
            'logger_name': record.filename,
            'exception': ''.join(traceback.format_exception(record.exc_info)),
        }
        return json.dumps(log_obj)