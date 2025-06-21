from sqlalchemy.exc import SQLAlchemyError
from app.dao.base import BaseDAO
from app.food.models import Food
from app.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession


class FoodDAO(BaseDAO):
    model = Food
