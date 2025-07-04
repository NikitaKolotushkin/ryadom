#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

import ryadom_schemas.events as schemas_events

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
        event = await service.get_event_by_id(event_id)
        return event

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/events/{event_id}", response_model=schemas_events.EventResponse, status_code=200)
async def update_event(request: Request, event_id: int, event_data: schemas_events.EventCreate, service: EventsService = Depends(get_events_service)):
    try:
        event = await service.update_event(event_id, event_data)
        return event
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/events/{event_id}", response_model=schemas_events.EventResponse, status_code=200)
async def delete_event(request: Request, event_id: int, service: EventsService = Depends(get_events_service)):
    try:
        event = await service.delete_event(event_id)
        return event
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))