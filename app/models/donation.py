from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean, Text, ForeignKey

from app.core.db import Base


class Donation(Base):
    """Класс пожертования."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime, default=None)
