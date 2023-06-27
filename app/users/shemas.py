from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    '''Схема для отображения пользователя.'''
    id: int
    email: EmailStr
    username: str


class UserCreate(schemas.BaseUserCreate):
    '''Схема для создания пользователя.'''
    email: EmailStr
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class AdminCreate(schemas.BaseUserCreate):
    '''Схема для создания пользователя админом.'''
    email: EmailStr
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool]
