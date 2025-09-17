#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import httpx
import os
import typing

import ryadom_schemas.users as schemas_users
import ryadom_schemas.auth as schemas_auth

from app.models.refresh_token import RefreshTokenModel
from app.models.user import UserModel

from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


class UsersService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self._pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)
    
    def verify_password(self, password: str, hash: str) -> bool:
        return self._pwd_context.verify(password, hash)

    async def create_user(self, user: schemas_users.UserCreate) -> schemas_users.UserResponse:
        """
        Создать нового пользователя

        Args:
            user: данные пользователя

        Returns:
            UserResponse: созданный пользователь
        """

        existing_user = await self.session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )

        if existing_user.scalar_one_or_none():
            raise ValueError(f'User with email {user.email} already exists')

        hashed_password = self.get_password_hash(user.password)

        user_data = user.model_dump(exclude={'password'})

        new_user = UserModel(
            **user_data, 
            password_hash=hashed_password,
            created_at=datetime.now().isoformat()
        )
        
        try:
            self.session.add(new_user)

            await self.session.commit()
            await self.session.refresh(new_user)

            return schemas_users.UserResponse.model_validate(new_user, from_attributes=True)
        
        except Exception as e:
            await self.session.rollback()

            raise ValueError('Database error')

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

    async def authenticate_user(self, email: str, password: str):
        """
        Проверить учетные данные и вернуть пользователя
        
        Args:
            email: электронная почта
            password: пароль
        
        Returns:
            User: данные пользователя
        """

        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )

        user = result.scalar_one_or_none()

        if not user or not self.verify_password(password, user.password_hash):
            return None

        return user
    
    async def create_refresh_token(self, user_id: int, remember_me: bool = False) -> str:
        """
        Создать refresh-токен

        Args:
            user_id: id пользователя
            remember_me: флаг \"запомнить меня\"

        Returns:
            token: refresh-токен
        """

        expires_delta = timedelta(days=int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')) if remember_me else 1)
        expires_at = datetime.now() + expires_delta

        token = str(uuid4())
    
        new_token = RefreshTokenModel(
            token=token,
            user_id=user_id,
            expires_at=expires_at,
        )

        self.session.add(new_token)

        await self.session.commit()
        await self.session.refresh(new_token)

        return token

    async def validate_refresh_token(self, token: str) -> schemas_users.UserResponse:
        """
        Проверить валидность refresh-токена и вернуть пользователя

        Args:
            token: refresh-токен

        Returns:
            UserResponse: пользователь
        """

        result = await self.session.execute(
            select(RefreshTokenModel)
            .where(RefreshTokenModel.token == token)
            .where(RefreshTokenModel.revoked == False)
            .where(RefreshTokenModel.expires_at > datetime.now())
        )

        db_token = result.scalar_one_or_none()

        if not db_token:
            raise ValueError('Invalid refresh token')
        

        result = await self.session.execute(
            select(UserModel).where(UserModel.id == db_token.user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise ValueError('User not found')
        
        return schemas_users.UserResponse.model_validate(user, from_attributes=True)
    
    async def revoke_refresh_token(self, token: str) -> None:
        """
        Отозвать refresh-токен

        Args:
            token: refresh-токен
        """
        await self.session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.token == token)
            .values(is_revoked=True)
        )

        await self.session.commit()
