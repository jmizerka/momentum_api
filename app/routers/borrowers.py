from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_borrower, delete_borrower, get_all_borrowers, get_borrower, update_borrower
from app.db.session import get_db
from app.schemas import BorrowerCreate, BorrowerFilter, BorrowerRead

borrowers_router = APIRouter(tags=["Borrowers"], prefix="/borrowers")


@borrowers_router.post("/", response_model=BorrowerRead)
async def create_borrower_endpoint(
    borrower: BorrowerCreate,
    session: AsyncSession = Depends(get_db),
):
    return await create_borrower(session, borrower.card_number)


@borrowers_router.get("/{borrower_id}", response_model=BorrowerRead)
async def get_borrower_endpoint(
    borrower_id: int,
    session: AsyncSession = Depends(get_db),
):
    db_borrower = await get_borrower(session, borrower_id)
    if not db_borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return db_borrower


@borrowers_router.get("/", response_model=list[BorrowerRead])
async def get_all_borrowers_endpoint(
    filters: BorrowerFilter = Depends(),
    session: AsyncSession = Depends(get_db),
):
    return await get_all_borrowers(
        session,
        skip=filters.skip,
        limit=filters.limit,
        card_number=filters.card_number,
    )


@borrowers_router.put("/{borrower_id}", response_model=BorrowerRead)
async def update_borrower_endpoint(
    borrower_id: int,
    new_data: BorrowerCreate,
    session: AsyncSession = Depends(get_db),
):
    db_borrower = await update_borrower(session, borrower_id, new_card_number=new_data.card_number)
    if not db_borrower:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return db_borrower


@borrowers_router.delete("/{borrower_id}")
async def delete_borrower_endpoint(
    borrower_id: int,
    session: AsyncSession = Depends(get_db),
):
    success = await delete_borrower(session, borrower_id)
    if not success:
        raise HTTPException(status_code=404, detail="Borrower not found")
    return {"detail": "Borrower deleted successfully"}
