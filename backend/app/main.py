import os
import asyncio
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze
from app.models.schemas import HealthResponse


# Self-ping to prevent Render free tier spin-down
async def keep_alive():
    """Ping self every 10 minutes to prevent Render from spinning down"""
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if not render_url:
        return  # Only run on Render
    
    await asyncio.sleep(60)  # Wait 1 minute after startup
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(f"{render_url}/health", timeout=30)
                print("Keep-alive ping successful")
            except Exception as e:
                print(f"Keep-alive ping failed: {e}")
            await asyncio.sleep(600)  # Ping every 10 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup: Start keep-alive task
    task = asyncio.create_task(keep_alive())
    yield
    # Shutdown: Cancel keep-alive task
    task.cancel()


app = FastAPI(
    title="AI Resume Analyzer",
    description="AI-powered resume analysis, classification, and experience estimation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend connection
# Read allowed origins from environment variable, default to all for dev
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
if cors_origins_env == "*":
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in cors_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router, tags=["Resume Analysis"])


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", message="API is running")

