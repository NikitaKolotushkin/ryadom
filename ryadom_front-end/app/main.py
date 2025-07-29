#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routes.routes import router


app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(router)


@app.exception_handler(404)
async def redirect_404(request: Request, exc):
    return RedirectResponse(url="/")