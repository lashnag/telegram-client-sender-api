import logging
import json
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_test_mode

def init_logger():
    logger = logging.getLogger()

    if is_test_mode:
        handler = logging.StreamHandler()
        level = logging.DEBUG
    else:
        handler = AsynchronousLogstashHandler(
            host='logstash',
            port=5022,
            database_path=None,
        )
        level = logging.INFO

    handler.setLevel(level)
    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler]
    )
    logging.root.addHandler(handler)
    logger.addHandler(handler)
    for handler in logging.root.handlers:
        handler.setLevel(level)

    logger.info(f"Test mode: {is_test_mode}")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'asctime': self.formatTime(record),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'filename': record.filename,
        }
        return json.dumps(log_obj)