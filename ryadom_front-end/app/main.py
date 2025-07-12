#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.routes import router


app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(router)