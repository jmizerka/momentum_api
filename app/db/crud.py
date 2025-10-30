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
