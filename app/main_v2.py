import logging
from logger import init_logger
from fastapi import FastAPI

init_logger()
logging.getLogger().info("Main v2 run")
server = FastAPI()