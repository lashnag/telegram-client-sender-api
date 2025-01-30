import logging
from logstash_async.handler import AsynchronousLogstashHandler
from environments_loader import is_test_mode

def init_logger():
    if is_test_mode:
        logstash_handlers = [logging.StreamHandler()]
    else:
        logstash_handlers = [
            AsynchronousLogstashHandler(
                host='logstash',
                port=5022,
                database_path=None
            )
        ]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=logstash_handlers
    )