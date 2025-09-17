#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator


Base = declarative_base()

DATABASE_URL = os.getenv("POSTGRES_USERS_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


from app.models.user import UserModel
from app.models.refresh_token import RefreshTokenModel


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session