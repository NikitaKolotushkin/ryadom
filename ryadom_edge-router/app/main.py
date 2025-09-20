#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.config import get_config
from app.routes.routes import router


config = get_config()

app = FastAPI(docs_url=config.DOCS_URL, redoc_url=config.REDOC_URL, openapi_url=config.OPENAPI_URL, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:8081',    # Dev front-end
        'https://ryadom-spbu.ru'    # Prod front-end
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=3600
)

app.include_router(router, prefix=config.API_PREFIX)