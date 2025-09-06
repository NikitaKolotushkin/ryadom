from .base import BaseConfig

import os


class DevelopmentConfig(BaseConfig):
    """Конфигурация для разработки"""
    DEVELOPMENT: bool = True
    DEBUG: bool = True
    RELOAD: bool = True

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"