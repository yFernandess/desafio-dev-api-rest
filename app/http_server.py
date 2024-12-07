import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
import uvicorn

from app.config.settings import Settings

from app.handlers.http.account_handler import AccountHandler
from app.handlers.http.transaction_handler import TransactionHandler


API_VERSION = "v1"


def create_app() -> FastAPI:
    app = FastAPI(
        title="Core Accounts API",
        description="Simple bank account management",
        version=API_VERSION,
    )

    app.include_router(
        AccountHandler().get_router(),
        prefix=f"/{API_VERSION}/accounts",
        tags=["AccountHandler"],
    )

    app.include_router(
        TransactionHandler().get_router(),
        prefix=f"/{API_VERSION}/transactions",
        tags=["TransactionHandler"],
    )

    return app


if __name__ == "__main__":  # pragma: no cover
    settings = Settings.get_settings()
    params = {"host": "0.0.0.0", "port": settings.fast_api_port}
    uvicorn.run(create_app(), **params)
