from datetime import datetime

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
    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="book", lazy="selectin")  # lazy loading would not work in async context
    __table_args__ = (CheckConstraint("serial_num ~ '^[0-9]{6}$'", name="check_serial_num_six_digits"),)


class Borrower(Base):
    __tablename__ = "borrowers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_number: Mapped[str] = mapped_column(String(6), index=True, unique=True)
    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="borrower", lazy="selectin")
    __table_args__ = (CheckConstraint("card_number ~ '^[0-9]{6}$'", name="check_card_number_six_digits"),)


class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    borrower_id: Mapped[int] = mapped_column(Integer, ForeignKey("borrowers.id"))
    borrow_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now)
    return_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    book: Mapped["Book"] = relationship("Book", back_populates="loans", lazy="selectin")
    borrower: Mapped["Borrower"] = relationship("Borrower", back_populates="loans", lazy="selectin")