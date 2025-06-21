from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk
from app.food.sql_enums import Product
from sqlalchemy import ForeignKey, text
from sqlalchemy import String


class Food(Base):
    id: Mapped[int_pk]
    product_name: Mapped[Product] = mapped_column(String, default=Product.BEET.name)
    students_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    calories: Mapped[int] = mapped_column(server_default=text('0'))
    students: Mapped["Student"] = relationship("Student", back_populates="food")
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_'))})"

