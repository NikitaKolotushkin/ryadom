from sqlalchemy import Column, Integer, String, Text, DateTime

from app.models.base import Base


class EventModel(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    category = Column(Text)
    format = Column(Text, nullable=False, default='online')
    name = Column(Text, nullable=False)
    description = Column(Text)
    photo = Column(Text)
    banner = Column(Text)
    location = Column(Text)
    address = Column(Text)
    date = Column(Text, nullable=False)
    start_time = Column(Text, nullable=False)
    max_participants = Column(Integer)
    color = Column(Text)
    created_at = Column(Text, nullable=False)
