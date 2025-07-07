from sqlalchemy import Boolean, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


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