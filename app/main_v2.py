import uvicorn
import logging
from controller import server
from logger import init_logger

init_logger()
logging.getLogger("main_v2").info("Сервер запущен")

uvicorn.run(server, host='0.0.0.0', port=4322)