import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_borrower, delete_borrower, get_all_borrowers, get_borrower, update_borrower
from app.db.session import get_db
from app.schemas import BorrowerCreate, BorrowerFilter, BorrowerRead

logger = logging.getLogger(__name__)


borrowers_router = APIRouter(tags=["Borrowers"], prefix="/borrowers")


@borrowers_router.post("/", response_model=BorrowerRead)
async def create_borrower_endpoint(
    borrower: BorrowerCreate,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Creating a new borrower with card_number=%s", borrower.card_number)
    try:
        db_borrower = await create_borrower(session, borrower.card_number)
        logger.info("Borrower created successfully with id=%s", db_borrower.id)
        return db_borrower
    except Exception as e:
        logger.error("Error creating borrower: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@borrowers_router.get("/{borrower_id}", response_model=BorrowerRead)
async def get_borrower_endpoint(
    borrower_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Fetching borrower with id=%s", borrower_id)
    try:
        db_borrower = await get_borrower(session, borrower_id)
    except Exception as e:
        logger.error("Error fetching borrower: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not db_borrower:
        logger.warning("Borrower not found with id=%s", borrower_id)
        raise HTTPException(status_code=404, detail="Borrower not found")
    logger.info("Borrower fetched successfully: id=%s", db_borrower.id)
    return db_borrower


@borrowers_router.get("/", response_model=list[BorrowerRead])
async def get_all_borrowers_endpoint(
    filters: BorrowerFilter = Depends(),
    session: AsyncSession = Depends(get_db),
):
    logger.info(
        "Fetching all borrowers with filters: skip=%s, limit=%s, card_number=%s",
        filters.skip, filters.limit, filters.card_number
    )
    try:
        borrowers = await get_all_borrowers(
        session,
        skip=filters.skip,
        limit=filters.limit,
        card_number=filters.card_number
        )
    except Exception as e:
        logger.error("Error fetching borrowers: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    logger.info("Fetched %d borrowers", len(borrowers))
    return borrowers


@borrowers_router.put("/{borrower_id}", response_model=BorrowerRead)
async def update_borrower_endpoint(
    borrower_id: int,
    new_data: BorrowerCreate,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Updating borrower id=%s with new card_number=%s", borrower_id, new_data.card_number)
    try:
        db_borrower = await update_borrower(session, borrower_id, new_card_number=new_data.card_number)
    except Exception as e:
        logger.error("Error updating borrower: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not db_borrower:
        logger.warning("Borrower not found for update: id=%s", borrower_id)
        raise HTTPException(status_code=404, detail="Borrower not found")
    logger.info("Borrower updated successfully: id=%s", db_borrower.id)
    return db_borrower



@borrowers_router.delete("/{borrower_id}")
async def delete_borrower_endpoint(
    borrower_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Deleting borrower with id=%s", borrower_id)
    try:
        success = await delete_borrower(session, borrower_id)
    except Exception as e:
        logger.error("Error deleting borrower: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not success:
        logger.warning("Borrower not found for deletion: id=%s", borrower_id)
        raise HTTPException(status_code=404, detail="Borrower not found")
    logger.info("Borrower deleted successfully: id=%s", borrower_id)
    return {"detail": "Borrower deleted successfully"}
