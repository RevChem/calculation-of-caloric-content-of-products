import os
import ssl   # Библиотека для шифрования (безопасного обмена данными между клиентом и сервером)
import redis
from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_PORT: int
    REDIS_HOST: str
    #REDIS_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

celery_app = Celery("celery_worker", broker=redis_url, backend=redis_url)
ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}
celery_app.conf.update(broker_use_ssl=ssl_options, redis_backend_use_ssl=ssl_options)


redis_client = redis.Redis(host=settings.REDIS_HOST,
                           port=settings.REDIS_PORT,
                           db=0, #password=settings.REDIS_PASSWORD,
                           ssl=False, ssl_cert_reqs=None)

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


