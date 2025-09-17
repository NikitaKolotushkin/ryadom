#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base


class UserModel(Base):
    __tablename__ = 'user_'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    is_spbsu_student = Column(Boolean, nullable=False, default=False)
    university = Column(Text)
    faculty = Column(Text)
    speciality = Column(Text)
    course = Column(Integer)
    photo = Column(Text)
    email_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(Text)

    refresh_token = relationship(
        'RefreshTokenModel', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
