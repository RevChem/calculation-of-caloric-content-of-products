import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from faststream.redis import RedisBroker
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_SSL: bool



    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


scheduler = AsyncIOScheduler(jobstores={'default': RedisJobStore(host=settings.REDIS_HOST,
                                                                 port=settings.REDIS_PORT,
                                                                 db=settings.REDIS_DB)}
                             )
broker = RedisBroker(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")