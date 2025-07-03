#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from httpx import HTTPStatusError
from fastapi import APIRouter, HTTPException, Request

from app.services.router_service import RouterService
import ryadom_schemas.events as schemas_events
import ryadom_schemas.users as schemas_users


router = APIRouter()
router_service = RouterService()


# USERS

@router.post('/users/', response_model=schemas_users.UserResponse)
async def post_event(request: Request, user: schemas_users.UserCreate):
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