import logging
import secrets

from typing import Annotated
from contextlib import asynccontextmanager

from uvicorn import server
from fastapi import FastAPI, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.exceptions import StarletteHTTPException, RequestValidationError, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.database import engine
from src.const import const
from src.models import model_user
from src.routers import (
    router_api
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown_event()


# Swagger, Redocly에 접근하는 권한 확인을 위해 환경변수 체크
env = const.ENV

app = FastAPI(
    title="JAVIS API Server",
    description="JAVIS the AI Secretary for you",
    lifespan=lifespan,
    docs_url=None if env == "prod" else "/docs",
    redoc_url=None if env == "prod" else "/redoc"
)

# Swagger-UI에 보안걸기
security = HTTPBasic()


def get_admin(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    correct_username = secrets.compare_digest(credentials.username, const.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, const.SWAGGER_PASSWORD)
    if not correct_username or not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Basic"}
        )
    return ""


@app.get(path="/docs", include_in_schema=False)
async def get_documentation(admin: str = Depends(get_admin)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="JAVIS API service")


@app.get("/redoc", include_in_schema=False)
async def get_redoc(admin: str = Depends(get_admin)):
    return get_redoc_html(openapi_url="/openapi.json", title="JAVIS API service")


@app.get(path="/openapi.json", include_in_schema=False)
async def get_openapi(admin: str = Depends(get_admin)):
    return get_openapi(title="JAVIS API service", version="0.1.0", routes=app.routes)


# Logging 설정
log = logging.getLogger(__name__)


# Generic Error handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Opps! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


app.add_middleware(middleware_class=DBSessionMiddleware, db_url=const.DB_URL)

# CORS
origins = ['*']

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def include_routers():
    print("Include routers...")
    app.include_router(router_api.router)


def init_database():
    print("Initializing database tables...")
    model_user.Base.metadata.create_all(bind=engine)

@app.get("/")
async def check_index():
    return {"status": "OK"}


# Startup event
async def startup():
    """
    Startup event
    :return:
    """
    banner = f"""       
        ██╗  ██╗██╗    ████████╗██╗  ██╗███████╗██████╗ ███████╗██╗
        ██║  ██║██║    ╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔════╝██║
        ███████║██║       ██║   ███████║█████╗  ██████╔╝█████╗  ██║
        ██╔══██║██║       ██║   ██╔══██║██╔══╝  ██╔══██╗██╔══╝  ╚═╝
        ██║  ██║██║       ██║   ██║  ██║███████╗██║  ██║███████╗██╗
        ╚═╝  ╚═╝╚═╝       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝
                                               from. L2Softlab
        """
    print(banner)
    print("JAVIS API start")

    # Including router
    include_routers()
    # Initialize database tables
    init_database()


async def shutdown_event():
    """
    Shutdown event
    :return:
    """
    goodbye_banner = f"""    
     ██████╗  ██████╗  ██████╗ ██████╗     ██████╗ ██╗   ██╗███████╗██╗
    ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗    ██╔══██╗╚██╗ ██╔╝██╔════╝██║
    ██║  ███╗██║   ██║██║   ██║██║  ██║    ██████╔╝ ╚████╔╝ █████╗  ██║
    ██║   ██║██║   ██║██║   ██║██║  ██║    ██╔══██╗  ╚██╔╝  ██╔══╝  ╚═╝
    ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝    ██████╔╝   ██║   ███████╗██╗
     ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝     ╚═════╝    ╚═╝   ╚══════╝╚═╝
                                by L2Softlab
    """
    print(goodbye_banner)
    print("Swit IMAP Satellite shutdown")


if __name__ == "__main__":
    server.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        loop="asyncio",
        reload=True,
        log_level=logging.INFO,
    )
