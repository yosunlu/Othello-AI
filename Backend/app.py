import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.routes import pvp_game_session_routes, login_routes

load_dotenv()
app = FastAPI()
app.include_router(login_routes.router)
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
    uvicorn.run(app, host='0.0.0.0', port=8000)
