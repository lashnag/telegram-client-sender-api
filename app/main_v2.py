from logger import init_logger
from fastapi import FastAPI
import logging
from message_reader import fetch_messages
from exceptions import InvalidGroupException
from fastapi.responses import JSONResponse

init_logger()
logging.getLogger().info("Main v2 run")
server = FastAPI()

@server.get('/get-subscription-messages')
async def process_data(subscription: str, last_message_id: int):
    try:
        logging.debug("Got request: " + subscription + " last message id: " + str(last_message_id))
        messages = await fetch_messages(subscription, last_message_id)
    except InvalidGroupException:
        return JSONResponse(content={'error': "Invalid group"}, status_code=403)
    except Exception as e:
        return JSONResponse(content={'error': f'Internal server error: {str(e)}'}, status_code=500)

    return JSONResponse(
        content={"messages": messages},
        status_code=200
    )