import logging
import json
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_test_mode

def init_logger():
    if is_test_mode:
        handler = logging.StreamHandler()
        logging.basicConfig(
            level=logging.DEBUG,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[handler]
        )
        logging.getLogger().addHandler(handler)
        for handler in logging.root.handlers:
            handler.setLevel(logging.DEBUG)
    else:
        handler = AsynchronousLogstashHandler(
            host='logstash',
            port=5022,
            database_path=None,
        )
        logging.basicConfig(
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[handler]
        )
        logging.getLogger().addHandler(handler)
        for handler in logging.root.handlers:
            handler.setLevel(logging.INFO)

    formatter = JsonFormatter()
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    logging.getLogger().info(f"Test mode: " + str(is_test_mode()))

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'asctime': self.formatTime(record),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'filename': record.filename,
        }
        return json.dumps(log_obj)