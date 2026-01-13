import os
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI

from app.config.cors_config import CorsConfig
from app.config.logging_config import LoggingConfig
from app.config.router_config import RoutesConfig
from app.config.db_config import engine, Base

# Import all entities to register them with Base.metadata
from app.example.models.entity.example_entity import ExampleEntity  # noqa: F401

# Load .env from config directory (relative to this file's location)
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup: Create all tables
    if os.getenv("AUTO_CREATE_TABLES", "True").lower() == "true":
        Base.metadata.create_all(bind=engine)
        LoggingConfig.get_logger().info("Database tables created/verified")
    yield
    # Shutdown: cleanup if needed
    LoggingConfig.get_logger().info("Application shutdown")


app = FastAPI(
    title=os.getenv("APP_TITLE", "FastAPI Service"),
    description=os.getenv("APP_DESCRIPTION", "FastAPI Backend Service Template"),
    lifespan=lifespan,
)

RoutesConfig(app)

cors_config = CorsConfig()
cors_config.init_cors(app)

if __name__ == "__main__":
    LoggingConfig.get_logger().info("Application START")

    uvicorn.run(
        app="main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        app_dir=".",
        port=int(os.getenv("PORT", "8080")),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        workers=int(os.getenv("WORKERS", 1)),
    )
