from fastapi import APIRouter, Depends, status

from app.core.dependencies import obter_usuario_atual
from app.domain.assinatura import Assinatura, AssinaturaCreate
from app.domain.usuario import Usuario
from app.services.assinatura_service import assinatura_service

router = APIRouter(prefix="/v1/assinaturas", tags=["Assinaturas"])


@router.get("", response_model=list[Assinatura])
def listar_assinaturas() -> list[Assinatura]:
    return assinatura_service.listar()


@router.get("/{assinatura_id}", response_model=Assinatura)
def buscar_assinatura(assinatura_id: int) -> Assinatura:
    return assinatura_service.buscar_por_id(assinatura_id)


@router.post("", response_model=Assinatura, status_code=status.HTTP_201_CREATED)
def criar_assinatura(
    dados: AssinaturaCreate,
    usuario: Usuario = Depends(obter_usuario_atual),
) -> Assinatura:
    return assinatura_service.criar(dados)
