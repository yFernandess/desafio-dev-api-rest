from starlette import status

from app.interfaces.exceptions import ExceptionInterface


class ExceptionMessageBuilder(Exception):
    def __init__(self, ex_info: ExceptionInterface):
        self.title = ex_info.title
        self.status_code = ex_info.status_code
        self.message = ex_info.message


class ObjectNotFound(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None, object_name: str = ""):
        ex_info = ex_info or ExceptionInterface(
            title="Objeto " + object_name + " não encontrado",
            message="Não foi possível encontrar o dado solicitado.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
        super(ObjectNotFound, self).__init__(ex_info=ex_info)
