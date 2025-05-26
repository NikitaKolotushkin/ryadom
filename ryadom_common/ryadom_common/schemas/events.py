from datetime import datetime
from pydantic import model_serializer, BaseModel, Field
from typing import List, Optional


class EventBase(BaseModel):
    '''
    Базовая модель с общими полями.
    '''
    name: str
    description: str


class EventCreate(EventBase):
    '''
    Модель для POST запросов (создания событий).
    Содержит поля, которые принимаются от клиента.
    '''
    location: str
    date: str
    max_participants: int
    color: str


class EventResponse(EventCreate):
    id: int
    created_at: str


class EventListResponse(BaseModel):
    events: List[EventResponse]