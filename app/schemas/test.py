from typing import Optional

from pydantic import BaseModel, Field, validator, PositiveInt, Extra

from .base import CommonBase

from datetime import datetime
from pydantic import BaseModel


class CommonBase(BaseModel):
    """Базовый класс схемы, от которого наследуем все остальные."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime

    class Config:
        orm_mode = True



class CharityProjectBase(BaseModel):
    """Базовый класс схемы для проектов, от которого наследуем все остальные."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    @validator('name')
    def name_not_empty(cls, value: str):
        if not value:
            raise ValueError('Не может быть пустым')
        return value

    @validator('description')
    def description_not_empty(cls, value: str):
        if not value:
            raise ValueError('Не может быть пустым')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CommonBase):
    pass
