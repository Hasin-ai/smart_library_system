from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
from sqlalchemy import text

from app.config.settings import settings
from app.config.database import engine, get_db
from app.models.loan import Base
from app.controllers.loan_controller import router as loan_router
from app.schemas.loan import HealthResponse
from app.clients.user_client import UserServiceClient
from app.clients.book_client import BookServiceClient
from app.core.logging import logger

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.SERVICE_NAME}")
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    yield
    logger.info(f"Shutting down {settings.SERVICE_NAME}")

# Create FastAPI app
app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.SERVICE_VERSION,
    description="Loan management service for the Smart Library System",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers
app.include_router(loan_router)

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Check database
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"
    finally:
        if 'db' in locals():
            db.close()
    
    # Check external services
    user_client = UserServiceClient()
    book_client = BookServiceClient()
    
    user_service_status = "healthy" if await user_client.check_health() else "unhealthy"
    book_service_status = "healthy" if await book_client.check_health() else "unhealthy"
    
    overall_status = "healthy"
    if db_status == "unhealthy":
        overall_status = "unhealthy"
    elif user_service_status == "unhealthy" or book_service_status == "unhealthy":
        overall_status = "degraded"
    
    return HealthResponse(
        status=overall_status,
        service=settings.SERVICE_NAME,
        version=settings.SERVICE_VERSION,
        database=db_status,
        user_service=user_service_status,
        book_service=book_service_status,
        timestamp=datetime.utcnow()
    )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
        "docs": "/docs",
        "health": "/health"
    }
