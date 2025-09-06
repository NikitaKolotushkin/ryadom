#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from app.config import get_config
from app.database import engine
from app.routes.routes import router
from app.models.event import Base


config = get_config()

app = FastAPI(docs_url=config.DOCS_URL, redoc_url=config.REDOC_URL, openapi_url=config.OPENAPI_URL)


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)