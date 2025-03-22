import re, uuid
from typing import Optional

from fastapi import HTTPException

from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import field_validator


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool

class UpdateUserRequest(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None

class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role: str

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name incorrect")
        return value
    
    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname incorrect")
        return value

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str = 'backlog'
    responsible: str

class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    responsible: str | None = None

class AddUserInTeam(BaseModel):
    ...

class Token(BaseModel):
    access_token: str
    token_type: str 