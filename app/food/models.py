from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk
from app.food.sql_enums import Product


class Food(Base):
    id: Mapped[int_pk]
    product_name: Mapped[str] # Mapped[Product] = mapped_column(default = Product.beet)

    students: Mapped["Student"] = relationship("Student", back_populates="food")
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_'))})"

