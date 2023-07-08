from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str = 'Описание Бронирование переговорок'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'qwerty123'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()