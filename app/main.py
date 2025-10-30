from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import init_db
from app.routers import books_router, borrowers_router, loans_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(borrowers_router)
app.include_router(books_router)
app.include_router(loans_router)
