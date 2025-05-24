from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):
    start = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    elapsed = time.time() - start
    logger.info(f"Response: {response.status_code} in {elapsed:.3f}s")
    response.headers["X-Process-Time"] = str(elapsed)
    return response

def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"],
    )
    app.middleware("http")(logging_middleware)
