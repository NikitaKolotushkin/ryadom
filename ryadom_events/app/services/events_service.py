#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import httpx
import typing

import ryadom_schemas.events as schemas_events

from app.models.event import EventModel

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class EventsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_event(self, event: schemas_events.EventCreate):
        """
        Создать новое событие

        Args:
            event: данные события

        Returns:
            EventResponse: созданное событие
        """

        new_event = EventModel(**event.model_dump(), created_at=datetime.now().isoformat())
        self.session.add(new_event)

        await self.session.commit()
        await self.session.refresh(new_event)

        return schemas_events.EventResponse.model_validate(new_event, from_attributes=True)

    async def get_all_events(self):
        """
        Получить все события
        
        Returns:
            EventListResponse: список событий
        """

        result = await self.session.execute(select(EventModel))
        
        events = result.scalars().all()

        return schemas_events.EventListResponse(
            events=[schemas_events.EventResponse.model_validate(event, from_attributes=True) for event in events]
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

        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )

        event = result.scalar_one_or_none()

        if not event:
            raise ValueError(f'Event with id {event_id} not found')
        
        return schemas_events.EventResponse.model_validate(event, from_attributes=True)

    async def update_event(self, event_id: int, event: schemas_events.EventCreate):
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
        
        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )

        db_event = result.scalar_one_or_none()

        if not db_event:
            raise ValueError(f'Event with id {event_id} not found')

        for key, value in event.model_dump().items():
            setattr(db_event, key, value)

        await self.session.commit()
        await self.session.refresh(db_event)

        return schemas_events.EventResponse.model_validate(db_event, from_attributes=True)

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

        result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )

        event = result.scalar_one_or_none()

        if not event:
            raise ValueError(f'Event with id {event_id} not found')

        await self.session.delete(event)
        await self.session.commit()

        return schemas_events.EventResponse.model_validate(event, from_attributes=True)
