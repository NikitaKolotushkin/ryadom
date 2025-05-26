#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from app.routes.routes import router


app = FastAPI()
app.include_router(router)