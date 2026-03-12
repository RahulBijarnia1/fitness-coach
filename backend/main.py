"""
FitCoach AI - Professional Fitness Analytics Platform

Main application entry point with comprehensive middleware setup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.settings import settings
from app.config.database import engine, Base
from app.core.logging import setup_logging, logger

# Import all models so SQLAlchemy registers them
from app.models.user import User       # noqa: F401
from app.models.profile import Profile # noqa: F401
from app.models.goal import Goal       # noqa: F401
from app.models.progress import ProgressLog  # noqa: F401

# Import middleware
from app.middleware.error_handler import setup_exception_handlers
from app.middleware.rate_limiter import setup_rate_limiting
from app.middleware.request_logger import RequestLoggingMiddleware

# Import API routers
from app.api.v1.router import api_router as api_v1_router

# Legacy routers (for backward compatibility)
from app.routers import auth_routes, user_routes, fitness_routes, progress_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    setup_logging(debug=settings.DEBUG)
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FitCoach AI")


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Setup exception handlers
setup_exception_handlers(app)

# Setup rate limiting
setup_rate_limiting(app)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Register API v1 routes (new versioned API)
app.include_router(api_v1_router, prefix=settings.API_PREFIX)

# Register legacy routes (backward compatibility with /api prefix)
LEGACY_PREFIX = "/api"
app.include_router(auth_routes.router, prefix=LEGACY_PREFIX, include_in_schema=False)
app.include_router(user_routes.router, prefix=LEGACY_PREFIX, include_in_schema=False)
app.include_router(fitness_routes.router, prefix=LEGACY_PREFIX, include_in_schema=False)
app.include_router(progress_routes.router, prefix=LEGACY_PREFIX, include_in_schema=False)


@app.get("/", tags=["Health"])
def root():
    """
    API root endpoint.
    
    Returns basic API information and status.
    """
    return {
        "success": True,
        "message": "FitCoach AI API is running",
        "data": {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "api_version": "v1",
            "docs": "/docs",
        }
    }


@app.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint.
    
    Returns API health status for monitoring.
    """
    return {
        "success": True,
        "status": "healthy",
        "version": settings.VERSION,
    }


@app.get("/api/health", tags=["Health"])
def api_health():
    """
    API health check endpoint.
    """
    return {
        "success": True,
        "status": "healthy",
        "api_version": "v1",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
    )
