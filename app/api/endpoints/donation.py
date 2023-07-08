from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.models import User
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
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
    response_model_exclude={'close_date', }
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Get запрос на получение всех пожертований."""
    reservations = await donation_crud.get_multi(session)
    return reservations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'invested_amount', 'fully_invested'},
    dependencies=[Depends(current_user)],
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Post запрос на создание пожертования."""
    new_donation = await donation_crud.create(donation, session)
    new_donation = await invest(
        new_donation.id, charity_project_crud,
        donation_crud, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    dependencies=[Depends(current_user)],
    response_model_exclude={
        'user_id', 'close_date',
        'fully_invested', 'invested_amount'
    },
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Get запрос на получение пожертований пользователя."""
    donations = await donation_crud.get_by_user(session, user)
    return donations
