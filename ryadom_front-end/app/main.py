#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_config
from app.routes.routes import router


config = get_config()

app = FastAPI(docs_url=config.DOCS_URL, redoc_url=config.REDOC_URL, openapi_url=config.OPENAPI_URL)

app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(router)


@app.exception_handler(404)
async def redirect_404(request: Request, exc):
    return RedirectResponse(url="/")