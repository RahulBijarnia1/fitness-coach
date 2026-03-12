"""
API v1 Router Configuration.

Aggregates all v1 API routes with proper prefixing and tags.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, fitness, progress, analytics

# Create main v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    fitness.router,
    prefix="/fitness",
    tags=["Fitness"],
)

api_router.include_router(
    progress.router,
    prefix="/progress",
    tags=["Progress"],
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"],
)
