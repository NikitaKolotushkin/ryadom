#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import httpx
import typing

import ryadom_schemas.events as schemas_events
import ryadom_schemas.members as schemas_members

from app.models.event import EventModel
from app.models.member import MemberModel

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class EventsService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.users_service_url = os.getenv("USERS_SERVICE_URL")

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

    async def add_member_to_event(self, event_id: int, member_data: schemas_members.MemberCreate) -> schemas_members.MemberResponse:
        """
        Добавить участника в событие

        Args:
            event_id: ID события
            member_data: данные участника (user_id и role)

        Returns:
            MemberResponse: добавленный участник

        Raises:
            ValueError: если событие не найдено, пользователь не найден или участник уже добавлен
        """
        event_result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        event = event_result.scalar_one_or_none()
        
        if not event:
            raise ValueError(f'Event with id {event_id} not found')

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f'{self.users_service_url}/users/{member_data.user_id}')
                
                if response.status_code == 404:
                    raise ValueError(f'User with id {member_data.user_id} not found')
                    
                response.raise_for_status()
        except httpx.RequestError as e:
            raise ValueError(f'Failed to connect to users service: {str(e)}')
        except httpx.HTTPStatusError as e:
            raise ValueError(f'Users service error: {e.response.status_code}')

        VALID_ROLES = {"participant", "organizer", "partner"}
        if member_data.role not in VALID_ROLES:
            raise ValueError(f'Invalid role. Valid roles are: {", ".join(VALID_ROLES)}')

        existing_member_result = await self.session.execute(
            select(MemberModel).where(
                MemberModel.user_id == member_data.user_id,
                MemberModel.event_id == event_id
            )
        )
        existing_member = existing_member_result.scalar_one_or_none()
        
        if existing_member:
            raise ValueError(f'User {member_data.user_id} is already a member of event {event_id}')

        new_member = MemberModel(
            user_id=member_data.user_id,
            event_id=event_id,
            role=member_data.role,
        )
        
        self.session.add(new_member)
        await self.session.commit()
        await self.session.refresh(new_member)

        return schemas_members.MemberResponse.model_validate(new_member, from_attributes=True)
    
    async def get_members_by_event_id(self, event_id: int):
        """
        Получить всех участников события
        
        Args:
            event_id: ID события
            
        Returns:
            MemberListResponse: список участников события
            
        Raises:
            ValueError: если событие не найдено
        """
        
        event_result = await self.session.execute(
            select(EventModel).where(EventModel.id == event_id)
        )
        event = event_result.scalar_one_or_none()
        
        if not event:
            raise ValueError(f'Event with id {event_id} not found')
        
        result = await self.session.execute(
            select(MemberModel).where(MemberModel.event_id == event_id)
        )
        members = result.scalars().all()
        
        return schemas_members.MemberListResponse(
            members=[schemas_members.MemberResponse.model_validate(member, from_attributes=True) for member in members]
        )