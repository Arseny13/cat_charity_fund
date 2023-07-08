from typing import Optional

from pydantic import Extra, PositiveInt

from .base import CommonBase
from datetime import datetime


class DonationBase(CommonBase):
    """Базовый класс схемы, от которого наследуем схемы для пожертования."""
    comment: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationBase):
    id: int
    full_amount: PositiveInt
    create_date: datetime
    comment: Optional[str]
    user_id: Optional[int]

    class Config:
        orm_mode = True
