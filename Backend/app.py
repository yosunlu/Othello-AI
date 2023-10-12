from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.communication import testservice, pvp_game_session_routes


app = FastAPI()
app.include_router(testservice.router)
app.include_router(pvp_game_session_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/')
def index():
    return "LET'S BREAK CS506"

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
