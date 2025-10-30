from typing import List, Optional

from pydantic import BaseModel, Field, constr


class BorrowerBase(BaseModel):
    card_number: constr(pattern=r"^\d{6}$") = Field(..., description="6-digit card number")


class BorrowerCreate(BorrowerBase):  # useful in case of feature extensions
    pass


class BorrowerRead(BaseModel):
    id: int
    card_number: str
    loans: Optional[List["LoanRead"]] = None

    class Config:
        from_attributes = True


class BorrowerFilter(BaseModel):
    skip: Optional[int] = Field(None, ge=0, description="Number of records to skip for pagination")
    limit: Optional[int] = Field(None, gt=0, description="Maximum number of records to return")
    card_number: Optional[str] = Field(None, description="Filter by borrower card number")
