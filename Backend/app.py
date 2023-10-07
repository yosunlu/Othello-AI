from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.services import testservice


app = FastAPI()
app.include_router(testservice.router)

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
