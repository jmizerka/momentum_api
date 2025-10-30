from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_loan, delete_loan, get_all_loans, get_loan, update_loan_return_date
from app.db.session import get_db
from app.schemas import LoanCreate, LoanFilter, LoanRead

loans_router = APIRouter(tags=["Loans"], prefix="/loans")


@loans_router.post("/", response_model=LoanRead)
async def create_loan_endpoint(
    loan: LoanCreate,
    session: AsyncSession = Depends(get_db),
):
    try:
        return await create_loan(session, loan.book_id, loan.borrower_id, loan.borrow_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@loans_router.get("/{loan_id}", response_model=LoanRead)
async def get_loan_endpoint(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
):
    db_loan = await get_loan(session, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan


@loans_router.get("/", response_model=list[LoanRead])
async def get_all_loans_endpoint(
    filters: LoanFilter = Depends(),
    session: AsyncSession = Depends(get_db),
):
    return await get_all_loans(
        session,
        skip=filters.skip,
        limit=filters.limit,
        borrower_card_number=filters.borrower_card_number,
        book_serial_num=filters.book_serial_num,
        returned=filters.returned,
    )


@loans_router.put("/{loan_id}/return", response_model=LoanRead)
async def update_loan_return_date_endpoint(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
):
    db_loan = await update_loan_return_date(session, loan_id, datetime.now())
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan


@loans_router.delete("/{loan_id}")
async def delete_loan_endpoint(
    loan_id: int,
    session: AsyncSession = Depends(get_db),
):
    success = await delete_loan(session, loan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"detail": "Loan deleted successfully"}
