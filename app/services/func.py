from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import Donation, CharityProject, User
from app.schemas.donation import DonationCreate


async def invest(
        project_in: DonationCreate,
        session: AsyncSession,
        #user: User,
):
    projects = await charity_project_crud.get_multi_not_closed(session)
    full_amount = project_in.dict(exclude_unset=True)['full_amount']
    print(projects)
    print(full_amount)
    return projects
    if 'full_amount' not in project_in:
        return charity_project
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if charity_project.invested_amount > project_in['full_amount']:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='требуемую сумму меньше внесённой.'
        )
    if charity_project.full_amount < project_in['full_amount']:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Параметр full_amount нельзя установить меньше текущего!'
        )
    return charity_project
