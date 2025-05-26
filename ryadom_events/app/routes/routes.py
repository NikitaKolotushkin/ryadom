#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing

from fastapi import APIRouter, HTTPException, Request

from app.services.events_service import EventsService
import ryadom_common.schemas.events as schemas_events


router = APIRouter()
events_service = EventsService()


@router.get("/events/", response_model=schemas_events.EventListResponse)
async def get_all_events(request: Request):
    events = await events_service.get_all_events()
    return events


@router.get("/events/{event_id}", response_model=schemas_events.EventResponse)
async def get_event_by_id(request: Request, event_id: int) -> typing.Dict | None:
    event = await events_service.get_event_by_id(event_id)

    if not event:
        raise HTTPException(status_code=404)
    
    return event


@router.post("/events/", response_model=schemas_events.EventResponse, status_code=201)
async def create_event(request: Request, event: schemas_events.EventCreate):
    try:
        return await events_service.create_event(event)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))