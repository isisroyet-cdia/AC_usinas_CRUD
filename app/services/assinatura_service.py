"""
Camada de Servico, AssinaturaService.
"""

from app.domain.assinatura import Assinatura, AssinaturaCreate
from app.domain.usina import StatusUsina
from app.repositories.assinatura_repository import AssinaturaRepository, assinatura_repository
from app.repositories.usina_repository import UsinaRepository, usina_repository
from app.services.usina_service import ErroDeNegocio


class AssinaturaService:
    def __init__(
        self,
        repository: AssinaturaRepository,
        usinas: UsinaRepository,
    ) -> None:
        self._repository = repository
        self._usinas = usinas

    def listar(self) -> list[Assinatura]:
        return self._repository.listar()

    def buscar_por_id(self, assinatura_id: int) -> Assinatura:
        assinatura = self._repository.buscar_por_id(assinatura_id)
        if assinatura is None:
            raise ErroDeNegocio(
                code="RECURSO_NAO_ENCONTRADO",
                message=f"Assinatura com id {assinatura_id} nao foi encontrada.",
                status=404,
            )
        return assinatura

    def criar(self, dados: AssinaturaCreate) -> Assinatura:
        usina = self._usinas.buscar_por_id(dados.usina_id)
        if usina is None:
            raise ErroDeNegocio(
                code="RECURSO_NAO_ENCONTRADO",
                message=f"Usina com id {dados.usina_id} nao foi encontrada.",
                status=404,
            )
        if usina.status == StatusUsina.inativa:
            raise ErroDeNegocio(
                code="USINA_INATIVA",
                message="Nao e permitido criar assinatura em usina inativa.",
                status=409,
            )
        return self._repository.criar(dados)


assinatura_service = AssinaturaService(assinatura_repository, usina_repository)
