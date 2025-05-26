#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import httpx
import typing

import ryadom_common.schemas.events as schemas_events

from datetime import datetime
from fastapi import HTTPException


class EventsService:

    def __init__(self):
        self.in_memory_data_base = {
            "events": [
                {
                    "id": 0,
                    "name": "Event 0",
                    "description": "Description 0",
                    "location": "Online",
                    "date": datetime.now().isoformat(),
                    "max_participants": 10,
                    "color": "#FF0000",
                    "created_at": datetime.now().isoformat(),
                },
        ]}

    async def get_all_events(self):
        return schemas_events.EventListResponse(
            events=[schemas_events.EventResponse(**event) for event in self.in_memory_data_base["events"]]
        )

    async def get_event_by_id(self, event_id: int):
        for event in self.in_memory_data_base["events"]:
            if event["id"] == event_id:
                return schemas_events.EventResponse(**event)
            
    async def create_event(self, event: schemas_events.EventCreate):
    
        new_event = schemas_events.EventResponse(id=1, created_at=datetime.now().isoformat(), **event.model_dump())

        self.in_memory_data_base["events"].append(new_event.model_dump())
        return new_event