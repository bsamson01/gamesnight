from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from prometheus_client import make_asgi_app

from app.core.config import settings
from app.core.redis_client import redis_client
from app.api.endpoints import auth, rooms, payments, games
from app.db.base import engine, Base
from app.websocket.socketio_app import create_socketio_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    
    # Connect to Redis
    await redis_client.connect()
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    print("Shutting down...")
    await redis_client.disconnect()
    await engine.dispose()


# Initialize Sentry if DSN is provided
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.1,
    )

# Create FastAPI app
app = FastAPI(
    title="GameNight API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Sentry middleware
if settings.SENTRY_DSN:
    app.add_middleware(SentryAsgiMiddleware)

# Mount Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(games.router, prefix="/api/games", tags=["games"])

# Create Socket.IO app
socketio_app = create_socketio_app()


@app.get("/")
async def root():
    return {"message": "GameNight API v1.0"}


@app.get("/health")
async def health_check():
    try:
        # Check Redis connection
        await redis_client.redis.ping()
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy",
        "redis": redis_status
    }


# Export for running with uvicorn
# Run with: uvicorn app.main:app --reload
# For Socket.IO support, use the socketio_app instead