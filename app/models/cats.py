from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Cat(BaseModel):
    __tablename__ = "cats"

    name: Mapped[str] = mapped_column(String, nullable=False)
    experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    missions: Mapped[list["Mission"]] = relationship(
        "Mission",
        back_populates="cat",
    )

    def __repr__(self) -> str:
        return f"<Cat(name={self.name})>"
