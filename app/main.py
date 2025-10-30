from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_db
from app.routers import books_router, borrowers_router, loans_router


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
