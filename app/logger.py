import logging
import json
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_test_mode

def init_logger():
    logging.basicConfig(
        level=logging.DEBUG if is_test_mode() else logging.INFO,
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger("app")
    logger.debug("foo")
    logger.info("bar")
    logger.info(f"Test mode: {is_test_mode()}")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'asctime': self.formatTime(record),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'filename': record.filename,
        }
        return json.dumps(log_obj)