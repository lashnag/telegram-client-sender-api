import logging
from logstash_async.handler import AsynchronousLogstashHandler

def init_logger():
    logstash_handler = AsynchronousLogstashHandler(
        host='logstash',
        port=5022,
        database_path=None
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logstash_handler]
    )