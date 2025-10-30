from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_book, delete_book, get_all_books, get_book, update_book
from app.db.session import get_db
from app.schemas import BookCreate, BookFilter, BookRead

books_router = APIRouter(tags=["Books"], prefix="/books")


@books_router.post("/", response_model=BookRead)
async def create_book_endpoint(
    book: BookCreate,
    session: AsyncSession = Depends(get_db),
):
    return await create_book(session, serial_num=book.serial_num, title=book.title, author=book.author)


@books_router.get("/{book_id}", response_model=BookRead)
async def get_book_endpoint(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    db_book = await get_book(session, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@books_router.get("/", response_model=list[BookRead])
async def get_all_books_endpoint(
    filters: BookFilter = Depends(),
    session: AsyncSession = Depends(get_db),
):
    return await get_all_books(
        session,
        skip=filters.skip,
        limit=filters.limit,
        serial_num=filters.serial_num,
        title=filters.title,
        author=filters.author,
    )


@books_router.put("/{book_id}", response_model=BookRead)
async def update_book_endpoint(
    book_id: int,
    book: BookCreate,
    session: AsyncSession = Depends(get_db),
):
    db_book = await update_book(
        session, book_id=book_id, serial_num=book.serial_num, title=book.title, author=book.author
    )
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@books_router.delete("/{book_id}")
async def delete_book_endpoint(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    success = await delete_book(session, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}
