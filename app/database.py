from datetime import datetime
from typing import Annotated

# func - Используется для вызова SQL-функций на уровне запросов
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

# declared_attr - Позволяет определять атрибуты модели динамически (полезно при наследовании моделей).

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from app.config import get_db_url

DATABASE_URL = get_db_url()

# Создаёт асинхронный движок для работы с БД
engine = create_async_engine(DATABASE_URL)
# Фабрика асинхронных сессий для взаимодействия с БД 
# expire_on_commit=False: Объекты не будут помечены как устаревшие после вызова commit(). Это может быть полезно в случаях, когда вы уверены, что данные в базе данных не изменяются другими процессами и хотите избежать дополнительных запросов к базе данных для повышения производительности.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


# AsyncAttrs Позволяет использовать асинхронные методы и атрибуты в моделях (нужен для ORM при работе с async).
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
