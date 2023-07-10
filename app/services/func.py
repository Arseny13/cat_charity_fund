from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import ModelType, CRUD_TYPE


def close_model(model: ModelType) -> ModelType:
    """Функция закрытия модели."""
    model.invested_amount = model.full_amount
    model.fully_invested = True
    model.close_date = datetime.utcnow()
    return model


async def invest(
        obj_id: int,
        crud_one: CRUD_TYPE,
        crud_two: CRUD_TYPE,
        session: AsyncSession,
) -> ModelType:
    """Корутина инверстирования"""
    objs_one = await crud_one.get_multi_not_closed(session)
    obj_two = await crud_two.get(obj_id, session)
    sum_obj_two = obj_two.full_amount - obj_two.invested_amount
    remainder = 0
    for id in objs_one:
        obj_one = await crud_one.get(id, session)
        remainder = obj_one.full_amount - obj_one.invested_amount
        if remainder > sum_obj_two:
            obj_one.invested_amount = obj_one.invested_amount + sum_obj_two
            obj_two = close_model(obj_two)
            session.add(obj_one)
            break
        else:
            sum_obj_two -= remainder
            obj_one = close_model(obj_one)
            session.add(obj_one)
    if sum_obj_two == 0:
        obj_two = close_model(obj_two)
    elif sum_obj_two > 0 and objs_one:
        obj_two.invested_amount = obj_two.invested_amount + sum_obj_two
    session.add(obj_two)
    await session.commit()
    await session.refresh(obj_two)

    return obj_two
