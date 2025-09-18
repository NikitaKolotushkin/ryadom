#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose import jwt, JWTError
from typing import Any, Dict, Final


JWT_SECRET_KEY: Final[str] = os.getenv('JWT_SECRET_KEY')
ALGORITHM: Final[str] = os.getenv('ALGORITHM', 'HS256')


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Создание access-токена с UTC-временем и проверкой окружения
    
    Args:
        data: Данные для включения в токен
    
    Returns:
        str: Подписанный JWT-токен
    
    Raises:
        RuntimeError: Если не заданы критические переменные окружения
    """

    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set")

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Декодирование и валидация JWT
    
    Args:
        token: JWT-токен из заголовка Authorization
    
    Returns:
        Dict: Декодированные данные токена (payload)
    
    Raises:
        HTTPException 401: При ошибках валидации
    """
    try:
        
        if not JWT_SECRET_KEY:
            raise RuntimeError("JWT_SECRET_KEY is not set")
        
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Системная ошибка аутентификации: {str(e)}"
        )
