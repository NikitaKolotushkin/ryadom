#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

import ryadom_schemas.events as schemas_events
import ryadom_schemas.members as schemas_members

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.events_service import EventsService


router = APIRouter(tags=['events'])


async def get_events_service(session: AsyncSession = Depends(get_async_session)):
    return EventsService(session)


@router.post("/events/", response_model=schemas_events.EventResponse, status_code=201)
async def create_event(request: Request, event: schemas_events.EventCreate, service: EventsService = Depends(get_events_service)):    
    try:
        return await service.create_event(event)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events/", response_model=schemas_events.EventListResponse)
async def get_all_events(request: Request, service: EventsService = Depends(get_events_service)):
    return await service.get_all_events()    


@router.get("/events/{event_id}", response_model=schemas_events.EventResponse)
async def get_event_by_id(request: Request, event_id: int, service: EventsService = Depends(get_events_service)) -> typing.Dict | None:
    try:
        return await service.get_event_by_id(event_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/events/{event_id}", response_model=schemas_events.EventResponse, status_code=200)
async def update_event(request: Request, event_id: int, event_data: schemas_events.EventCreate, service: EventsService = Depends(get_events_service)):
    try:
        return await service.update_event(event_id, event_data)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/events/{event_id}", response_model=schemas_events.EventResponse, status_code=200)
async def delete_event(request: Request, event_id: int, service: EventsService = Depends(get_events_service)):
    try:
        return await service.delete_event(event_id)
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/events/{event_id}/members/", response_model=schemas_members.MemberResponse, status_code=201)
async def add_member_to_event(
    request: Request, 
    event_id: int, 
    member_data: schemas_members.MemberCreate, 
    service: EventsService = Depends(get_events_service)
) -> schemas_members.MemberResponse:
    """
    Добавить участника в событие
    
    Args:
        event_id: ID события из URL-пути
        member: данные участника (user_id и role)
    
    Returns:
        MemberResponse: информация о добавленном участнике
    """
    try:
        return await service.add_member_to_event(event_id, member_data)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/events/{event_id}/members/", response_model=schemas_members.MemberListResponse)
async def get_members_by_event_id(request: Request, event_id: int, service: EventsService = Depends(get_events_service)):
    try:
        return await service.get_members_by_event_id(event_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))