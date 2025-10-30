from typing import Optional

from pydantic import BaseModel, Field, constr


class BookBase(BaseModel):
    serial_num: constr(pattern=r"^\d{6}$") = Field(..., description="6-digit serial number")
    title: str
    author: str


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    serial_num: str
    title: str
    author: str
    loans: Optional[list["LoanRead"]] = None

    class Config:
        from_attributes = True


class BookFilter(BaseModel):
    skip: Optional[int] = Field(None, ge=0, description="Number of records to skip for pagination")
    limit: Optional[int] = Field(None, gt=0, description="Maximum number of records to return")
    serial_num: Optional[str] = Field(None, description="Filter by book serial number")
    title: Optional[str] = Field(None, description="Filter by book title")
    author: Optional[str] = Field(None, description="Filter by book author")
