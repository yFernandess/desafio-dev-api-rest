from fastapi import status

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import logging

from app.config.exceptions.general import ExceptionMessageBuilder
from app.interfaces.transaction import RequestDepositInterface, RequestWithdrawInterface
from app.services.transaction_service import TransactionService

from app.utils import generate_error_response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
router = InferringRouter()


@cbv(router)
class TransactionHandler:
    def __init__(
        self,
    ):
        self.transaction_service = TransactionService()

    @staticmethod
    def get_router():
        return router

    @router.post(
        "/deposit",
        description="Deposit an amount to an account",
        status_code=status.HTTP_201_CREATED,
        tags=["TransactionHandler"],
    )
    async def deposit(self, payload: RequestDepositInterface):
        try:
            response = await self.transaction_service.deposit(payload=payload)
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
        "/withdraw",
        description="Withdraw an amount from an account",
        status_code=status.HTTP_201_CREATED,
        tags=["TransactionHandler"],
    )
    async def withdraw(self, payload: RequestWithdrawInterface):
        try:
            response = await self.transaction_service.withdraw(payload=payload)
            return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
        except ExceptionMessageBuilder as ex:
            return JSONResponse(
                content={"title": ex.title, "message": ex.message},
                status_code=ex.status_code,
            )
        except Exception as err:
            logger.error(f"Failed {err}")
            return generate_error_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})
