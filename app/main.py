from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_db
from app.routers import books_router, borrowers_router, loans_router
from app.utils.setup_logging import setup_logging

setup_logging("library_api")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production origins would be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(borrowers_router)
app.include_router(books_router)
app.include_router(loans_router)
