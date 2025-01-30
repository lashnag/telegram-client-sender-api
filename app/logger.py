import logging
import json
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_test_mode

def init_logger():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if is_test_mode:
        logging.basicConfig(
            level=logging.DEBUG,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.StreamHandler()]
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                AsynchronousLogstashHandler(
                    host='logstash',
                    port=5022,
                    database_path=None
                )
            ]
        )

    formatter = JsonFormatter()
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    logging.getLogger("logger").info(f"Тестовый режим логгера " + str(is_test_mode()))

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'asctime': self.formatTime(record),
            'levelname': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_obj, ensure_ascii=False)