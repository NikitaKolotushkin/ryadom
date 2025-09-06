from .development import DevelopmentConfig
from .production import ProductionConfig

import os


def get_config():
    """
    Возвращает конфигурацию в зависимости от ENVIRONMENT
    Использование: from config import get_config; config = get_config()
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env not in ["development", "production"]:
        raise RuntimeError(
            f"Invalid ENVIRONMENT: {env}. Use 'development' or 'production'"
        )
    
    config = ProductionConfig() if env == "production" else DevelopmentConfig()
    
    return config