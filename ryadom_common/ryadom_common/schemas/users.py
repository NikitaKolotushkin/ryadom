from pydantic import BaseModel

class User(BaseModel):
    id: int


class UserCreate(BaseModel):
    id: int


class UserResponse(BaseModel):
    id: int