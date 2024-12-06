from __future__ import annotations

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import logging

from app.config.exceptions.general import ExceptionMessageBuilder
from app.interfaces.account import (
    RequestBlockAccountInterface,
    RequestCloseAccountInterface,
    RequestCreateAccountInterface,
    RequestUnblockAccountInterface,
)
from app.interfaces.account_owner import RequestCreateAccountOwnerInterface, RequestRemoveAccountOwnerInterface
from app.services.account_service import AccountService

from app.utils import generate_error_response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
router = InferringRouter()


@cbv(router)
class AccountHandler:
    def __init__(
        self,
    ):
        self._account_service = AccountService()

    @staticmethod
    def get_router():
        return router

    @router.post(
        "/owner",
        description="Create a new account owner",
        status_code=status.HTTP_201_CREATED,
        tags=["AccountHandler"],
    )
    async def create_owner(self, payload: RequestCreateAccountOwnerInterface):
        try:
            response = await self._account_service.create_owner(payload=payload)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})

    @router.delete(
        "/owner/{cpf}",
        description="Remove a account owner",
        status_code=status.HTTP_200_OK,
        tags=["AccountHandler"],
    )
    async def remove_owner(self, payload: RequestRemoveAccountOwnerInterface):
        try:
            await self._account_service.remove_owner(payload=payload)
            return JSONResponse(content="Account owner successfully removed", status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})

    @router.post(
        "/create",
        description="Create a new account",
        status_code=status.HTTP_201_CREATED,
        tags=["AccountHandler"],
    )
    async def create_account(self, payload: RequestCreateAccountInterface):
        try:
            response = await self._account_service.create_account(payload=payload)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})

    @router.get(
        "/{account_id}",
        description="Get account by account_id",
        status_code=status.HTTP_200_OK,
        tags=["AccountHandler"],
    )
    async def get_account(self, account_id: int):
        try:
            response = await self._account_service.get_account(account_id=account_id)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})

    @router.post(
        "/block",
        description="Block an account",
        status_code=status.HTTP_200_OK,
        tags=["AccountHandler"],
    )
    async def block_account(self, payload: RequestBlockAccountInterface):
        try:
            response = await self._account_service.block_account(payload=payload)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})

    @router.post(
        "/unblock",
        description="Unblock an account",
        status_code=status.HTTP_200_OK,
        tags=["AccountHandler"],
    )
    async def unblock_account(self, payload: RequestUnblockAccountInterface):
        try:
            response = await self._account_service.unblock_account(payload=payload)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})

    @router.post(
        "/close",
        description="Close an account",
        status_code=status.HTTP_200_OK,
        tags=["AccountHandler"],
    )
    async def close_account(self, payload: RequestCloseAccountInterface):
        try:
            response = await self._account_service.close_account(payload=payload)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})
