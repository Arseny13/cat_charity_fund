from typing import Optional

from pydantic import Extra, PositiveInt

from .base import CommonBase


class DonationBase(CommonBase):
    comment: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass
    #full_amount: PositiveInt


class DonationDB(DonationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
