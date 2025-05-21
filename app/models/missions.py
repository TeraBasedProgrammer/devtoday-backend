import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Target(BaseModel):
    __tablename__ = "targets"

    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    mission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("missions.id", ondelete="CASCADE"), nullable=False
    )

    mission: Mapped["Mission"] = relationship(back_populates="targets")

    def __repr__(self) -> str:
        return f"<Target(name={self.name})>"


class Mission(BaseModel):
    __tablename__ = "missions"

    cat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cats.id"), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    targets: Mapped[list[Target]] = relationship(Target, back_populates="mission")
    cat: Mapped["Cat"] = relationship(back_populates="missions")

    def __repr__(self) -> str:
        return f"<Mission(cat_id={self.cat_id})>"
