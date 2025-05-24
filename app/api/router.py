from fastapi import APIRouter
from app.modules.users.routes import router as users_router
from app.modules.books.routes import router as books_router
from app.modules.loans.routes import router as loans_router
from app.modules.statistics.routes import router as stats_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(books_router)
api_router.include_router(loans_router)
api_router.include_router(stats_router)
