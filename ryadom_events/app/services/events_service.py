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
        """
        Получить все события
        
        Returns:
            EventListResponse: список событий
        """
        return schemas_events.EventListResponse(
            events=[schemas_events.EventResponse(**event) for event in self.in_memory_data_base["events"]]
        )

    async def get_event_by_id(self, event_id: int):
        """
        Получить событие по его id
        
        Args:
            event_id: id события
        
        Returns:
            EventResponse: событие

        Raises:
            ValueError: если событие не было найдено
        """
        
        event_to_return = None
        
        for event in self.in_memory_data_base["events"]:
            if event["id"] == event_id:
                event_to_return = event
                break

        if not event_to_return:
            raise ValueError(f'event with id {event_id} not found')

        return schemas_events.EventResponse(**event)
            
    async def create_event(self, event: schemas_events.EventCreate):
        """
        Создать новое событие

        Args:
            event: данные события

        Returns:
            EventResponse: созданное событие
        """
        new_event = schemas_events.EventResponse(id=1, created_at=datetime.now().isoformat(), **event.model_dump())

        self.in_memory_data_base["events"].append(new_event.model_dump())
        return new_event
    
    async def update_event(self, event_id: int, event_data: schemas_events.EventCreate):
        """
        Обновить событие по его id

        Args:
            event_id: id события
            event: данные события

        Returns:
            EventResponse: обновленное событие

        Raises:
            ValueError: если событие не было найдено
        """

        event_to_update = None

        for event in self.in_memory_data_base["events"]:
            if event["id"] == event_id:
                event_to_update = event
                break

        if not event_to_update:
            raise ValueError(f'event with id {event_id} not found')

        event_to_update.update(event_data.model_dump())
        return schemas_events.EventResponse(**event_to_update)

    async def delete_event(self, event_id: int):
        """
        Удалить событие по его id
        
        Args:
            event_id: id события
        
        Returns:
            EventResponse: событие

        Raises:
            ValueError: если событие не было найдено
        """

        event_to_delete = None

        for event in self.in_memory_data_base["events"]:
            if event["id"] == event_id:
                event_to_delete = event
                break

        if not event_to_delete:
            raise ValueError(f'event with id {event_id} not found')
        
        self.in_memory_data_base["events"].remove(event)
        return schemas_events.EventResponse(**event_to_delete)
