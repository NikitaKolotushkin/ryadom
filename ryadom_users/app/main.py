#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from app.database import engine
from app.routes.routes import router
from app.models.user import Base


app = FastAPI()


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)