#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

from fastapi import APIRouter, HTTPException, Request

from app.services.events_service import EventsService
import ryadom_common.schemas.events as schemas_events


router = APIRouter()
events_service = EventsService()


@router.post("/events/", response_model=schemas_events.EventResponse, status_code=201)
async def create_event(request: Request, event: schemas_events.EventCreate):
    try:
        return await events_service.create_event(event)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events/", response_model=schemas_events.EventListResponse)
async def get_all_events(request: Request):
    events = await events_service.get_all_events()
    return events


@router.get("/events/{event_id}", response_model=schemas_events.EventResponse)
async def get_event_by_id(request: Request, event_id: int) -> typing.Dict | None:
    try:
        event = await events_service.get_event_by_id(event_id)
        return event

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/events/{event_id}", response_model=schemas_events.EventResponse, status_code=200)
async def update_event(request: Request, event_id: int, event_data: schemas_events.EventCreate):
    try:
        event = await events_service.update_event(event_id, event_data)
        return event
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/events/{event_id}", response_model=schemas_events.EventResponse, status_code=200)
async def delete_event(request: Request, event_id: int):
    try:
        event = await events_service.delete_event(event_id)
        return event
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))