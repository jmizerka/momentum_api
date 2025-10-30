from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LoanBase(BaseModel):
    borrow_date: Optional[datetime] = None
    return_date: Optional[datetime] = None


class LoanCreate(LoanBase):
    book_id: int
    borrower_id: int


class LoanRead(LoanBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None
    book_id: int
    borrower_id: int

    class Config:
        from_attributes = True  # allows to create pydantic model instance directly from orm model instance


class LoanFilter(BaseModel):
    skip: Optional[int] = Field(None, ge=0, description="Number of records to skip for pagination")
    limit: Optional[int] = Field(None, gt=0, description="Maximum number of records to return")
    borrower_card_number: Optional[str] = Field(None, description="Filter by borrower card number")
    book_serial_num: Optional[str] = Field(None, description="Filter by book serial number")
    returned: Optional[bool] = Field(None, description="Filter by return status (true/false)")
