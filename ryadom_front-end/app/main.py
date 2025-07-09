from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.services.front_end_service import router


app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(router)