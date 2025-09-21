#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from httpx import HTTPStatusError
from fastapi import APIRouter, Cookie, HTTPException, Response, Request

from app.services.router_service import RouterService
import ryadom_schemas.auth as schemas_auth
import ryadom_schemas.events as schemas_events
import ryadom_schemas.members as schemas_members
import ryadom_schemas.users as schemas_users


router = APIRouter()
router_service = RouterService()


# USERS

@router.post('/users/', response_model=schemas_users.UserResponse)
async def post_user(request: Request, user: schemas_users.UserCreate):
    try:
        user_data = await router_service.post_user_to_user_service(user)
        return user_data
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/users/')
async def get_users(request: Request):
    try:
        users_data = await router_service.get_all_users_from_user_service()
        return users_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/users/{user_id}')
async def get_user(request: Request, user_id: int):
    try:
        user_data = await router_service.get_user_from_user_service(user_id)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/users/{user_id}')
async def update_user(request: Request, user_id: int, user_data: schemas_users.UserCreate):
    try:
        user_data_ = await router_service.update_user_from_user_service(user_id, user_data)
        return user_data_
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/users/{user_id}')
async def delete_user(request: Request, user_id: int):
    try:
        user_data = await router_service.delete_user_from_user_service(user_id)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.post('/auth/login', response_model=dict)
async def login(request: Request, login_data: schemas_auth.LoginRequest, response: Response):
    try:
        token_data = await router_service.login_user_from_user_service(login_data)

        response.set_cookie(
            key='access_token',
            value=token_data['access_token'],
            httponly=True,
            secure=request.url.scheme == 'https',   # True в проде
            samesite='lax',
            max_age=token_data['expires_in']
        )

        refresh_max_age = 60 * 60 * 24 * int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', 30))
        response.set_cookie(
            key='refresh_token',
            value=token_data['refresh_token'],
            httponly=True,
            secure=request.url.scheme == 'https',
            samesite='lax',
            max_age=refresh_max_age
        )

        return {
            'status': 'success',
            'expires_in': token_data['expires_in']
        }
    
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, 
            detail=e.response.json().get('detail', 'Ошибка аутентификации')
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/auth/refresh', response_model=dict)
async def refresh_access_token(request: Request, response: Response, refresh_token: str = Cookie(None, alias='refresh_token')):
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh токен не найден')
    
    try:
        token_data = await router_service.refresh_token_from_user_service(refresh_token)

        response.set_cookie(
            key='access_token',
            value=token_data['access_token'],
            httponly=True,
            secure=request.url.scheme == 'https',
            samesite='lax',
            max_age=token_data['expires_in']
        )

        return {
            'status': 'success',
            'expires_in': token_data['expires_in']
        }
    
    except HTTPStatusError as e:
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        raise HTTPException(
            status_code=e.response.status_code, 
            detail='Token refresh failed'
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post('/auth/logout', response_model=dict)
async def logout(request: Request, response: Response, refresh_token: str = Cookie(None, alias='refresh_token')):
    if refresh_token:
        await router_service.logout_user_from_user_service(refresh_token)

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return {'detail': 'Successfully logged out'}


# EVENTS    

@router.post('/events/', response_model=schemas_events.EventResponse)
async def post_event(request: Request, event: schemas_events.EventCreate):
    try:
        event_data = await router_service.post_event_to_event_service(event)
        return event_data
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/events/')
async def get_events(request: Request):
    try:
        events_data = await router_service.get_all_events_from_event_service()
        return events_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/events/{event_id}')
async def get_event(request: Request, event_id: int):
    try:
        event_data = await router_service.get_event_from_event_service(event_id)
        return event_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/events/{event_id}')
async def update_event(request: Request, event_id: int, event_data: schemas_events.EventCreate):
    try:
        event_data_ = await router_service.update_event_from_event_service(event_id, event_data)
        return event_data_
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/events/{event_id}')
async def delete_event(request: Request, event_id: int):
    try:
        event_data = await router_service.delete_event_from_event_service(event_id)
        return event_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/events/{event_id}/members/', response_model=schemas_members.MemberResponse)
async def add_member_to_event(request: Request, event_id: int, member: schemas_members.MemberCreate):
    try:
        member_data = await router_service.add_member_to_event_from_event_service(event_id, member)
        return member_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get('/events/{event_id}/members/')
async def get_members_by_event_id(request: Request, event_id: int):
    try:
        members_data = await router_service.get_members_by_event_id_from_event_service(event_id)
        return members_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# MAPS

@router.get('/geocode')
async def get_coordinates_by_address(request: Request, address: str):
    try:
        coordinates = await router_service.get_coordinates_by_address(address)
        return coordinates
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get('/static-map')
async def get_static_map(request: Request, lat: float, lon: float, zoom: int, size: str):
    try:
        static_map = await router_service.get_static_map_url_by_coordinates(lat, lon, zoom, size)
        return static_map
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
