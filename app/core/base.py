"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base, CommonBase # noqa
from app.models import CharityProject, User  # noqa

# alembic revision --autogenerate -m "Add table reservation"
# alembic upgrade head
# alembic downgrade base