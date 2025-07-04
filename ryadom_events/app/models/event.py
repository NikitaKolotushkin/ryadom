from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class EventModel(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    photo = Column(String(255))
    location = Column(String(255))
    date = Column(String(63), nullable=False)
    max_participants = Column(Integer)
    color = Column(String(7))
    created_at = Column(String(63), nullable=False)
