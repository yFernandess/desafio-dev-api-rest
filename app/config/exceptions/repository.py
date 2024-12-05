from app.config.exceptions.general import ExceptionMessageBuilder
from app.interfaces.exceptions import ExceptionInterface


class MultipleUpsertsException(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None):
        ex_info = ex_info or ExceptionInterface(
            title="Multiplos objetos serão atualizados",
            message="Ajuste a sua busca ou passe o parametro upsert_many " "como True",
            status_code=400,
        )
        super(MultipleUpsertsException, self).__init__(ex_info=ex_info)


class MultipleDeletesException(ExceptionMessageBuilder):
    def __init__(self, ex_info: ExceptionInterface = None):
        ex_info = ex_info or ExceptionInterface(
            title="Multiplos objetos serão deletados",
            message="Ajuste a sua busca ou passe o parametro delete_many " "como True",
            status_code=400,
        )
        super(MultipleDeletesException, self).__init__(ex_info=ex_info)
