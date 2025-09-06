from .base import BaseConfig

import os


class ProductionConfig(BaseConfig):
    """Конфигурация для продакшена"""
    DEVELOPMENT: bool = False
    DEBUG: bool = False
    RELOAD: bool = False