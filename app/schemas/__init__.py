from app.schemas.book import BookBase, BookCreate, BookFilter, BookRead
from app.schemas.borrower import BorrowerBase, BorrowerCreate, BorrowerFilter, BorrowerRead
from app.schemas.loan import LoanBase, LoanCreate, LoanFilter, LoanRead

BookRead.model_rebuild()
BorrowerRead.model_rebuild()
LoanRead.model_rebuild()
