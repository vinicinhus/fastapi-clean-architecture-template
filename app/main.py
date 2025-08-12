from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from app.api.v1.routes import auth, role, user
from app.core.logging import logger
from app.db.seed.role_seed import init_roles
from app.db.seed.user_seed import init_admin_user
from app.db.session import engine, init_db
from app.middleware.response_size_logger import ResponseSizeLoggerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager.

    Initializes the database, seeds default roles, and creates
    an admin user if it does not exist. Handles any exceptions
    during startup gracefully.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        AsyncGenerator[None, None]: Allows FastAPI to handle the application lifecycle.
    """
    try:
        init_db()
        with Session(engine) as session:
            init_roles(session)
            init_admin_user(session)
        yield
    except Exception as e:
        logger.error(f"Error during application lifespan: {e}")
        yield


# Initialize FastAPI application with the custom lifespan handler
app = FastAPI(lifespan=lifespan)

app.add_middleware(ResponseSizeLoggerMiddleware)

# Register API routes
app.include_router(auth.router)
app.include_router(role.router)
app.include_router(user.router)
