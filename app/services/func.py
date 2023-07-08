from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


def close_model(model):
    setattr(model, 'invested_amount', model.full_amount)
    setattr(model, 'fully_invested', True)
    setattr(model, 'close_date', datetime.utcnow())
    return model


async def invest(
        donate_id: int,
        session: AsyncSession,
):
    projects = await charity_project_crud.get_multi_not_closed(session)
    donate = await donation_crud.get(donate_id, session)
    sum_donate = donate.full_amount - donate.invested_amount
    remainder = 0
    for id in projects:
        project = await charity_project_crud.get(id, session)
        remainder = project.full_amount - project.invested_amount
        if remainder > sum_donate:
            setattr(project, 'invested_amount', project.invested_amount + sum_donate)
            sum_donate -= remainder
            session.add(project)
            break
        else:
            sum_donate -= remainder
            project = close_model(project)
            session.add(project)
    if remainder + sum_donate == 0:
        donate = close_model(donate)
    elif sum_donate > 0:
        setattr(donate, 'invested_amount', donate.full_amount - sum_donate)
    else:
        setattr(donate, 'invested_amount', remainder + sum_donate)

    session.add(donate)
    await session.commit()
    await session.refresh(donate)

    return donate


async def invest_for_project(
        project_id: int,
        session: AsyncSession,
):
    donations = await donation_crud.get_multi_not_closed(session)
    project = await charity_project_crud.get(project_id, session)
    sum_project = project.full_amount - project.invested_amount
    remainder = 0
    for id in donations:
        donate = await donation_crud.get(id, session)
        remainder = donate.full_amount - donate.invested_amount
        if remainder >= sum_project:
            setattr(donate, 'invested_amount', donate.invested_amount + sum_project)
            sum_project -= remainder
            session.add(donate)
            break
        else:
            sum_project -= remainder
            donate = close_model(donate)
            session.add(donate)
    if sum_project == 0:
        project = close_model(project)
    elif sum_project > 0:
        setattr(project, 'invested_amount', project.full_amount - sum_project)
    else:
        setattr(project, 'invested_amount', remainder + sum_project)

    session.add(project)
    await session.commit()
    await session.refresh(project)

    return project