from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.domain.usuario import Usuario
from app.services.auth_service import auth_service
from app.services.usina_service import ErroDeNegocio

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login", auto_error=False)


def obter_usuario_atual(token: str | None = Depends(oauth2_scheme)) -> Usuario:
    if token is None:
        raise ErroDeNegocio(
            code="TOKEN_INVALIDO",
            message="Token ausente, invalido ou expirado.",
            status=401,
        )
    return auth_service.usuario_do_token(token)
