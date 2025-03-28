from fastapi import FastAPI

from app.services.front_end_service import router


app = FastAPI()
app.include_router(router)