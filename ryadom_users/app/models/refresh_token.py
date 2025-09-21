#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Boolean, Column, DateTime,  ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base


class RefreshTokenModel(Base):
    __tablename__ = 'refresh_token'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user_.id'), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)
    is_revoked = Column(Boolean, nullable=False, default=False)

    user = relationship('UserModel', back_populates='refresh_token')
