#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from datetime import datetime, timedelta
from jose import jwt


def create_access_token(data: dict) -> str:
    """
    Создание access-токена

    Args:
        data: данные токена

    Returns:
        str: access-токен
    """
    
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, 
        os.getenv('JWT_SECRET_KEY'), 
        algorithm=os.getenv('ALGORITHM')
    )
