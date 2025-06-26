"""

Mapped[] - Тип для аннотации отображаемых атрибутов

mapped_column() - Определяет колонку БД и её параметры

Annotated - Связывает тип и метаданные (для переиспользования). Позволяет объединить тип (Mapped) и метаданные (например, ограничения или типы БД) в одной аннотации

Field - Дополнительные параметры отображения (init, repr и др.)

"""

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date
from app.food.models import Food


# создаем модель таблицы студентов
class Student(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    enrollment_year: Mapped[int]
    course: Mapped[int]
    photo: Mapped[str] = mapped_column(Text, nullable=True)
    special_notes: Mapped[str_null_true]
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=False)
    food_id: Mapped[int | None] = mapped_column(ForeignKey("foods.id"), nullable=True)

    # Определяем отношения: один студент имеет один факультет
    major: Mapped["Major"] = relationship("Major", back_populates="students")
    food: Mapped["Food"] = relationship("Food", back_populates="students")

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_'))})"


# преобразует объект модели (например, пользователя) в словарь, где ключи — это названия полей, а значения — данные из объекта. Удобно использовать с библиотекой pydantic. Явно указываются какие поля будут включены
    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "address": self.address,
            "enrollment_year": self.enrollment_year,
            "course": self.course,
            "special_notes": self.special_notes,
            "major_id": self.major_id,
            "food_id": self.food_id,
            'photo': self.photo
        }
