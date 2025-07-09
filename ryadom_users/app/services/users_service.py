#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import httpx
import typing

import ryadom_schemas.users as schemas_users

from app.models.user import UserModel

from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UsersService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self._pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)
    
    def verify_password(self, password: str, hash: str) -> bool:
        return self._pwd_context.verify(password, hash)

    async def create_user(self, user: schemas_users.UserCreate):
        """
        Создать нового пользователя

        Args:
            user: данные пользователя

        Returns:
            UserResponse: созданный пользователь
        """

        hashed_password = self.get_password_hash(user.password)

        # new_user = UserModel(**user.model_dump(exclude={'password'}), password_hash=hashed_password, created_at=datetime.now().isoformat())
        # new_user = UserModel(**user.model_dump(), created_at=datetime.now().isoformat())

        user_data = user.model_dump(exclude={'password'})

        new_user = UserModel(
            **user_data, 
            password_hash=hashed_password,
            created_at=datetime.now().isoformat()
        )
        
        self.session.add(new_user)

        await self.session.commit()
        await self.session.refresh(new_user)

        return schemas_users.UserResponse.model_validate(new_user, from_attributes=True)

    async def get_all_users(self):
        """
        Получить всех пользователей
        
        Returns:
            UserListResponse: список пользователей
        """

        result = await self.session.execute(select(UserModel))
        
        users = result.scalars().all()

        return schemas_users.UserListResponse(
            users=[schemas_users.UserResponse.model_validate(user, from_attributes=True) for user in users]
        )

    async def get_user_by_id(self, user_id: int):
        """
        Получить пользователя по его id
        
        Args:
            user_id: id пользователя
        
        Returns:
            UserResponse: пользователь

        Raises:
            ValueError: если пользователь не был найден
        """

        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f'User with id {user_id} not found')
        
        return schemas_users.UserResponse.model_validate(user, from_attributes=True)

    async def update_user(self, user_id: int, user: schemas_users.UserCreate):
        """
        Обновить данные пользователя по его id

        Args:
            user_id: id пользователя
            user: данные пользователя

        Returns:
            UserResponse: обновленный пользователь

        Raises:
            ValueError: если пользователь не был найден
        """
        
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )

        db_user = result.scalar_one_or_none()

        if not db_user:
            raise ValueError(f'User with id {user_id} not found')

        for key, value in user.model_dump().items():
            setattr(db_user, key, value)

        await self.session.commit()
        await self.session.refresh(db_user)

        return schemas_users.UserResponse.model_validate(db_user, from_attributes=True)

    async def delete_user(self, user_id: int):
        """
        Удалить пользователя по его id
        
        Args:
            user_id: id пользователя
        
        Returns:
            UserResponse: пользователь

        Raises:
            ValueError: если пользователь не был найден
        """

        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f'User with id {user_id} not found')

        await self.session.delete(user)
        await self.session.commit()

        return schemas_users.UserResponse.model_validate(user, from_attributes=True)
