#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Request

from app.services.router_service import RouterService


router = APIRouter()
router_service = RouterService()


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
    

@router.get('/events/')
async def get_events(request: Request):
    try:
        events_data = await router_service.get_all_events_from_event_service()
        return events_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.post('/events/')
async def post_event(request: Request, event_data: dict):
    try:
        event_data = await router_service.post_event_to_event_service(event_data)
        return event_data
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
async def update_event(request: Request, event_id: int, event_data: dict):
    try:
        event_data = await router_service.update_event_from_event_service(event_id, event_data)
        return event_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/events/{event_id}')
async def delete_event(request: Request, event_id: int):
    try:
        event_data = await router_service.delete_event_from_event_service(event_id)
        return event_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))