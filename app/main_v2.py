import uvicorn
import logging
from controller import server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger().setLevel(logging.INFO)
logging.info("Сервер запущен")

uvicorn.run(server, host='0.0.0.0', port=4322)