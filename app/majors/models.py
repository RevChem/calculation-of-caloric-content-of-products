from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, str_null_true


# создаем модель таблицы факультетов (majors)
class Major(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    # Определяем отношения: один факультет может иметь много студентов
    students: Mapped[list["Student"]] = relationship("Student", back_populates="major")
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_'))})"

