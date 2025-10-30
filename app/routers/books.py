import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_book, delete_book, get_all_books, get_book, update_book
from app.db.session import get_db
from app.schemas import BookCreate, BookFilter, BookRead


logger = logging.getLogger(__name__)

books_router = APIRouter(tags=["Books"], prefix="/books")


@books_router.post("/", response_model=BookRead)
async def create_book_endpoint(
    book: BookCreate,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Creating a new book with serial_num=%s, title=%s", book.serial_num, book.title)
    try:
        db_book = await create_book(session, serial_num=book.serial_num, title=book.title, author=book.author)
        logger.info("Book created successfully with id=%s", db_book.id)
        return db_book
    except Exception as e:
        logger.error("Error creating book: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@books_router.get("/{book_id}", response_model=BookRead)
async def get_book_endpoint(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Fetching book with id=%s", book_id)
    try:
        db_book = await get_book(session, book_id)
    except Exception as e:
        logger.error("Error fetching book: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not db_book:
        logger.warning("Book not found with id=%s", book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("Book fetched successfully: id=%s", db_book.id)
    return db_book


@books_router.get("/", response_model=list[BookRead])
async def get_all_books_endpoint(
    filters: BookFilter = Depends(),
    session: AsyncSession = Depends(get_db),
):
    logger.info(
        "Fetching all books with filters: skip=%s, limit=%s, serial_num=%s, title=%s, author=%s",
        filters.skip, filters.limit, filters.serial_num, filters.title, filters.author
    )
    try:
        books = await get_all_books(
            session,
            skip=filters.skip,
            limit=filters.limit,
            serial_num=filters.serial_num,
            title=filters.title,
            author=filters.author,
        )
        logger.info("Fetched %d books", len(books))
        return books
    except Exception as e:
        logger.error("Error fetching all books: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@books_router.put("/{book_id}", response_model=BookRead)
async def update_book_endpoint(
    book_id: int,
    book: BookCreate,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Updating book id=%s with data: serial_num=%s, title=%s", book_id, book.serial_num, book.title)
    try:
        db_book = await update_book(
            session, book_id=book_id, serial_num=book.serial_num, title=book.title, author=book.author
        )
    except Exception as e:
        logger.error("Error updating book: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not db_book:
        logger.warning("Book not found for update: id=%s", book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("Book updated successfully: id=%s", db_book.id)
    return db_book


@books_router.delete("/{book_id}")
async def delete_book_endpoint(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Deleting book with id=%s", book_id)
    success = await delete_book(session, book_id)
    if not success:
        logger.warning("Book not found for deletion: id=%s", book_id)
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("Book deleted successfully: id=%s", book_id)
    return {"detail": "Book deleted successfully"}