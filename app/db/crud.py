from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Book, Loan, Borrower


async def create_book(session: AsyncSession, serial_num: str, title: str, author: str) -> Book:
    book = Book(serial_num=serial_num, title=title, author=author)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_book(session: AsyncSession, book_id: int) -> Book | None:
    result = await session.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def get_all_books(
    session: AsyncSession,
    skip: int | None = None,
    limit: int | None = None,
    serial_num: int | None = None,
    title: str | None = None,
    author: str | None = None,
) -> list[Book]:
    query = select(Book).options(selectinload(Book.loans).selectinload(Loan.borrower))  # load nested objects

    if serial_num:
        query = query.where(Book.serial_num == serial_num)
    if title:
        query = query.where(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    result = await session.execute(query)
    return result.scalars().all()


async def update_book(
    session: AsyncSession, book_id: int, serial_num: str = None, title: str = None, author: str = None
) -> Book | None:
    book = await get_book(session, book_id)
    if not book:
        return None
    if title:
        book.title = title
    if author:
        book.author = author
    if serial_num:
        book.serial_num = serial_num
    await session.commit()
    await session.refresh(book)
    return book


async def delete_book(session: AsyncSession, book_id: int) -> bool:
    book = await get_book(session, book_id)
    if not book:
        return False
    await session.delete(book)
    await session.commit()
    return True


async def create_borrower(session: AsyncSession, card_number: str) -> Borrower:
    borrower = Borrower(card_number=card_number)
    session.add(borrower)
    await session.commit()
    await session.refresh(borrower)
    return borrower


async def get_borrower(session: AsyncSession, borrower_id: int) -> Borrower | None:
    result = await session.execute(select(Borrower).where(Borrower.id == borrower_id))
    return result.scalar_one_or_none()


async def get_all_borrowers(
    session: AsyncSession,
    skip: int | None = None,
    limit: int | None = None,
    card_number: str | None = None,
) -> list[Borrower]:
    query = select(Borrower).options(selectinload(Borrower.loans).selectinload(Loan.book))
    if card_number:
        query = query.where(Borrower.card_number == card_number)
    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    result = await session.execute(query)
    return result.scalars().all()


async def update_borrower(session: AsyncSession, borrower_id: int, new_card_number: str) -> Borrower | None:
    borrower = await get_borrower(session, borrower_id)
    if not borrower:
        return None
    borrower.card_number = new_card_number
    await session.commit()
    await session.refresh(borrower)
    return borrower


async def delete_borrower(session: AsyncSession, borrower_id: id) -> bool:
    borrower = await get_borrower(session, borrower_id)
    if not borrower:
        return False
    await session.delete(borrower)
    await session.commit()
    return True


async def create_loan(session: AsyncSession, book_id: int, borrower_id: int, borrow_date: datetime = None) -> Loan:
    borrow_date = borrow_date or datetime.now()
    book = await get_book(session, book_id)
    borrower = await get_borrower(session, borrower_id)
    if not book or not borrower:
        raise ValueError("Book or Borrower not found")

    loan = Loan(borrow_date=borrow_date, book_id=book.id, borrower_id=borrower.id)
    loan.book = book
    loan.borrower = borrower
    session.add(loan)
    await session.commit()
    await session.refresh(loan)
    return loan


async def get_loan(session: AsyncSession, loan_id: int) -> Loan | None:
    return await session.get(Loan, loan_id)


async def get_all_loans(
    session: AsyncSession,
    skip: int | None = None,
    limit: int | None = None,
    borrower_card_number: str | None = None,
    book_serial_num: str | None = None,
    returned: bool | None = None,
) -> list[Loan]:
    query = select(Loan).options(selectinload(Loan.borrower), selectinload(Loan.book))

    if borrower_card_number:
        query = query.join(Loan.borrower).where(Borrower.card_number == borrower_card_number)
    if book_serial_num:
        query = query.join(Loan.book).where(Book.serial_num == book_serial_num)
    if returned is not None:
        if returned:
            query = query.where(Loan.return_date.is_not(None))
        else:
            query = query.where(Loan.return_date.is_(None))

    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def update_loan_return_date(session: AsyncSession, loan_id: int, return_date: datetime) -> Loan | None:
    loan = await get_loan(session, loan_id)
    if not loan:
        return None
    loan.return_date = return_date
    await session.commit()
    await session.refresh(loan)
    return loan


async def delete_loan(session: AsyncSession, loan_id: int) -> bool:
    loan = await get_loan(session, loan_id)
    if not loan:
        return False
    await session.delete(loan)
    await session.commit()
    return True