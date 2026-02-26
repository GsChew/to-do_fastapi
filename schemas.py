from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SUserCreate(BaseModel):
    email: str
    password: str


class SUser(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SUserInDB(SUser):
    hashed_password: str


class STaskAdd(BaseModel):
    title: str
    description: str
    status: str
    deadline: datetime | None


class STask(STaskAdd):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class STaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    deadline: datetime | None = None
