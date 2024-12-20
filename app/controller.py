from message_reader import fetch_messages
from exceptions import InvalidGroupException
from fastapi import FastAPI
from fastapi.responses import JSONResponse

server = FastAPI()

@server.get('/get-subscription-messages')
async def process_data(subscription: str, last_message_id: int):
    try:
        messages, last_message_id = await fetch_messages(subscription, last_message_id)
    except InvalidGroupException:
        return JSONResponse(content={'error': "Invalid group"}, status_code=403)
    except Exception as e:
        return JSONResponse(content={'error': f'Internal server error: {str(e)}'}, status_code=500)

    return JSONResponse(
        content={"messages": messages, "lastMessageId": last_message_id},
        status_code=200
    )