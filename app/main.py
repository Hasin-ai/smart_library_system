from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.core.middleware import setup_middleware
from app.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Smart Library System API"
)

setup_middleware(app)
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Smart Library System API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
