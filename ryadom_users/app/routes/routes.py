#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

import ryadom_schemas.users as schemas_users
import ryadom_schemas.auth as schemas_auth

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.users_service import UsersService


router = APIRouter(tags=['users'])


async def get_users_service(session: AsyncSession = Depends(get_async_session)):
    return UsersService(session)


@router.post("/users/", response_model=schemas_users.UserResponse, status_code=201)
async def create_user(request: Request, user: schemas_users.UserCreate, service: UsersService = Depends(get_users_service)):    
    try:
        return await service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/", response_model=schemas_users.UserListResponse)
async def get_all_users(request: Request, service: UsersService = Depends(get_users_service)):
    return await service.get_all_users()    


@router.get("/users/{user_id}", response_model=schemas_users.UserResponse)
async def get_user_by_id(request: Request, user_id: int, service: UsersService = Depends(get_users_service)) -> typing.Dict | None:
    try:
        user = await service.get_user_by_id(user_id)
        return user

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/users/{user_id}", response_model=schemas_users.UserResponse, status_code=200)
async def update_user(request: Request, user_id: int, user_data: schemas_users.UserCreate, service: UsersService = Depends(get_users_service)):
    try:
        user = await service.update_user(user_id, user_data)
        return user
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{user_id}", response_model=schemas_users.UserResponse, status_code=200)
async def delete_user(request: Request, user_id: int, service: UsersService = Depends(get_users_service)):
    try:
        user = await service.delete_user(user_id)
        return user
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# AUTH

@router.post('/auth/login', response_modes=schemas_auth.TokenResponse)
async def login(
    request: Request,
    login_data: schemas_auth.LoginRequest,
    session: AsyncSession = Depends(get_async_session),
    service: UsersService = Depends(get_users_service)
):
    try:
        pass
    
    except ValueError as e:
        pass
    
    except Exception as e:
        pass