import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv

envPath = Path('.') / 'Backend' / '.conf' / '.env'
load_dotenv(dotenv_path=envPath)

from src.routes import pvp_game_session_routes, login_routes

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

app.mount("/", StaticFiles(directory="Backend/src/frontend"), name="static")

@app.get('/')
def index():
    return "LET'S BREAK CS506"

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
