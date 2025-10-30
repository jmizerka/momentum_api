from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_loan, delete_loan, get_all_loans, get_loan, update_loan_return_date
from app.db.session import get_db
from app.schemas import LoanCreate, LoanFilter, LoanRead


logger = logging.getLogger(__name__)


loans_router = APIRouter(tags=["Loans"], prefix="/loans")


@loans_router.post("/", response_model=LoanRead)
async def create_loan_endpoint(
    loan: LoanCreate,
    session: AsyncSession = Depends(get_db),
):
    logger.info(
        "Creating a new loan: book_id=%s, borrower_id=%s, borrow_date=%s",
        loan.book_id, loan.borrower_id, loan.borrow_date
    )
    try:
        db_loan = await create_loan(session, loan.book_id, loan.borrower_id, loan.borrow_date)
        logger.info("Loan created successfully with id=%s", db_loan.id)
        return db_loan
    except Exception as e:
        logger.error("Unexpected error creating loan: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@loans_router.get("/{loan_id}", response_model=LoanRead)
async def get_loan_endpoint(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Fetching loan with id=%s", loan_id)
    db_loan = await get_loan(session, loan_id)
    if not db_loan:
        logger.warning("Loan not found with id=%s", loan_id)
        raise HTTPException(status_code=404, detail="Loan not found")
    logger.info("Loan fetched successfully: id=%s", db_loan.id)
    return db_loan


@loans_router.get("/", response_model=list[LoanRead])
async def get_all_loans_endpoint(
    filters: LoanFilter = Depends(),
    session: AsyncSession = Depends(get_db),
):
    logger.info(
        "Fetching all loans with filters: skip=%s, limit=%s, borrower_card_number=%s, book_serial_num=%s, returned=%s",
        filters.skip, filters.limit, filters.borrower_card_number, filters.book_serial_num, filters.returned
    )
    try:
        loans = await get_all_loans(
            session,
            skip=filters.skip,
            limit=filters.limit,
            borrower_card_number=filters.borrower_card_number,
            book_serial_num=filters.book_serial_num,
            returned=filters.returned,
        )
    except Exception as e:
        logger.error("Unexpected error fetching loans: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    logger.info("Fetched %d loans", len(loans))
    return loans



@loans_router.put("/{loan_id}/return", response_model=LoanRead)
async def update_loan_return_date_endpoint(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Updating return date for loan id=%s", loan_id)
    try:
        db_loan = await update_loan_return_date(session, loan_id, datetime.now())
    except Exception as e:
        logger.error("Unexpected error updating loan: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not db_loan:
        logger.warning("Loan not found for return update: id=%s", loan_id)
        raise HTTPException(status_code=404, detail="Loan not found")
    logger.info("Loan return date updated successfully: id=%s", db_loan.id)
    return db_loan


@loans_router.delete("/{loan_id}")
async def delete_loan_endpoint(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
):
    logger.info("Deleting loan with id=%s", loan_id)
    try:
        success = await delete_loan(session, loan_id)
    except Exception as e:
        logger.error("Unexpected error updating loan: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not success:
        logger.warning("Loan not found for deletion: id=%s", loan_id)
        raise HTTPException(status_code=404, detail="Loan not found")
    logger.info("Loan deleted successfully: id=%s", loan_id)
    return {"detail": "Loan deleted successfully"}
