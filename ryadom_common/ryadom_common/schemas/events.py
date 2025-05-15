from datetime import datetime
from pydantic import BaseModel
from typing import List


class EventBase(BaseModel):
    id: int
    name: str
    description: str | None = None


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    created_at: datetime


class EventListResponse(BaseModel):
    events: List[EventResponse]