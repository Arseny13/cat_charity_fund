from typing import Optional, List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    """Класс круд для CharityProject, унаследованный от CRUDBase."""

    async def get_multi_not_closed(
            self,
            session: AsyncSession
    ) -> List[CharityProject]:
        charity_projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested is False
            )
        )
        return charity_projects.scalars().all()

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def check_attr_project(
        self,
        project: CharityProject,
        session: AsyncSession
    ) -> CharityProject:
        obj_data = jsonable_encoder(project)
        if obj_data['invested_amount'] == obj_data['full_amount']:
            setattr(project, 'fully_invested', True)
        if project.fully_invested:
            setattr(project, 'close_date', datetime.utcnow())
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
