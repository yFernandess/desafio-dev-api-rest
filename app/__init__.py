from starlette.responses import JSONResponse


def generate_error_response(*, status_code: int, content: dict) -> JSONResponse:
    return JSONResponse(
        content=content,
        status_code=status_code,
    )
