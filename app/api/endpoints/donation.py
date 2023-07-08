from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.models import User
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB
)
from app.services.func import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
):
    reservations = await donation_crud.get_multi(session)
    return reservations


@router.post(
    '/',
    response_model=DonationDB,
    #response_model_exclude_none=True,
    #dependencies=[Depends(current_user)],
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        #user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session)
    res = await invest(donation, session)
    return new_donation
