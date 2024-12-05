from typing import Any, Optional

from pydantic import BaseModel
from starlette import status


class ExceptionInterface(BaseModel):
    title: Optional[str] = "Erro desconhecido"
    status_code: Optional[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: Optional[
        Any
    ] = "Ocorreu um erro na sua operação. Se o problema persistir entre em contato com o suporte."
