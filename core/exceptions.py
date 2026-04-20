from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []

    for err in exc.errors():
        campo = err["loc"][-1]

        if campo == "email":
            errores.append("Ingresá un email válido")
        elif campo == "clave":
            errores.append("La contraseña es obligatoria")
        else:
            errores.append(err["msg"])

    return JSONResponse(
        status_code=422,
        content={"detail": errores}
    )