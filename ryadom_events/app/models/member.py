from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey

from app.models.base import Base


class MemberModel(Base):
    __tablename__ = 'member'
    
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='_user_event_uc'),
    )   

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False, index=True) 
    role = Column(String(50), nullable=False)
