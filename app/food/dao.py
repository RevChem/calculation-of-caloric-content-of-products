from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.food.models import Food
from app.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from sqlalchemy import select
from app.food.models import Food  


class FoodDAO:
    model = Food

    @classmethod
    async def _get_calories(cls, product_name: str) -> float:
        """Получает калорийность продукта по его названию."""
        async with async_session_maker() as session:
            query = select(cls.model.calories).filter_by(product_name=product_name)
            result = await session.execute(query)
            calories = result.scalar_one_or_none()
            if calories is None:
                raise ValueError(f"Продукт '{product_name}' не найден в базе данных")
            return calories

    @classmethod
    async def add(cls, session, product_name: str, calories: float):
        """Добавляет запись о продукте в БД."""
        new_food = cls.model(
            product_name=product_name,
            calories=calories
        )
        session.add(new_food)
        return new_food