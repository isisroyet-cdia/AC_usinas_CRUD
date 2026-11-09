"""
Ponto de entrada da aplicacao.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.controllers.assinatura_controller import router as assinatura_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.usina_controller import router as usina_router
from app.services.usina_service import ErroDeNegocio

app = FastAPI(
    title="Bulbe Energia, API de Usinas",
    description="Handson de CRUD em FastAPI com autenticacao JWT e testes.",
    version="1.1.0",
)

app.include_router(auth_router)
app.include_router(usina_router)
app.include_router(assinatura_router)


@app.exception_handler(ErroDeNegocio)
def tratar_erro_de_negocio(request: Request, exc: ErroDeNegocio) -> JSONResponse:
    headers = {"WWW-Authenticate": "Bearer"} if exc.status == 401 else None
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "status": exc.status,
            }
        },
        headers=headers,
    )


@app.exception_handler(RequestValidationError)
def tratar_erro_de_validacao(request: Request, exc: RequestValidationError) -> JSONResponse:
    mensagens = []
    for erro in exc.errors():
        loc = ".".join(str(parte) for parte in erro.get("loc", []) if parte != "body")
        detalhe = erro.get("msg", "Dados invalidos.")
        mensagens.append(f"{loc}: {detalhe}" if loc else str(detalhe))

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "ERRO_DE_VALIDACAO",
                "message": "; ".join(mensagens) or "Dados invalidos.",
                "status": 422,
            }
        },
    )


@app.get("/", tags=["Status"])
def raiz() -> dict:
    return {"mensagem": "API de Usinas no ar. Acesse /docs para o Swagger."}
