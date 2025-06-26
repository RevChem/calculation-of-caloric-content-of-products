from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.food.models import Food
from app.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession


class FoodDAO(BaseDAO):
    model = Food

    @staticmethod
    async def add(session: AsyncSession, id: int, product_name: str):
        food_entry = Food(
            id = id,
            product_name = product_name
        )
        session.add(food_entry)