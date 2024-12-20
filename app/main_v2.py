import uvicorn
from controller import server

uvicorn.run(server, host='0.0.0.0', port=4322)