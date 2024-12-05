import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

# from app.handlers.http.account_handler import AccountHandler

from app.config.settings import Settings

# from app.database import db
from app.handlers.http.account_handler import AccountHandler


API_VERSION = "v1"


def create_app() -> FastAPI:
    app = FastAPI(
        title="Core Boiler API",
        description="Base for new microsservices",
        version=API_VERSION,
    )

    app.include_router(
        AccountHandler().get_router(),
        prefix=f"/{API_VERSION}/accounts",
        tags=["AccountHandler"],
    )

    return app


if __name__ == "__main__":  # pragma: no cover
    settings = Settings.get_settings()
    params = {"host": "0.0.0.0", "port": settings.fast_api_port}
    uvicorn.run(create_app(), **params)
