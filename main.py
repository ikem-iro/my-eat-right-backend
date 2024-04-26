from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from auth import auth_route
from users import user_route
from utils.config_utils import settings
from sqlmodel import SQLModel
from utils.db_utils import engine
from starlette.middleware.base import BaseHTTPMiddleware
from middleware.log_middleware import log_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A function that is called on startup. It creates all metadata for the SQLModel using the provided engine.
    """
    SQLModel.metadata.create_all(engine)
    yield






app = FastAPI(title="Eat-Right API", version="0.1.0", openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc", description="Api for Eat-Right", lifespan=lifespan)

@app.get('/')
async def home():
    return RedirectResponse('/docs')

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.include_router(auth_route.router, prefix=settings.API_V1_STR)
app.include_router(user_route.router, prefix=settings.API_V1_STR)




# @app.on_event("startup")
# async def startup() -> None:
#     """
#     A function that is called on startup. It creates all metadata for the SQLModel using the provided engine.
#     """
#     SQLModel.metadata.create_all(engine)