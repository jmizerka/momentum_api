from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    serial_num: Mapped[str] = mapped_column(String(6), unique=True, index=True)  # indexing for future filtering option
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author: Mapped[str] = mapped_column(String, nullable=False, index=True)