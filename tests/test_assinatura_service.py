import pytest

from app.domain.assinatura import AssinaturaCreate
from app.domain.usina import StatusUsina, UsinaCreate, UsinaUpdate
from app.repositories.assinatura_repository import InMemoryAssinaturaRepository
from app.repositories.usina_repository import InMemoryUsinaRepository
from app.services.assinatura_service import AssinaturaService
from app.services.usina_service import ErroDeNegocio, UsinaService


@pytest.fixture
def usinas() -> InMemoryUsinaRepository:
    return InMemoryUsinaRepository()


@pytest.fixture
def service(usinas: InMemoryUsinaRepository) -> AssinaturaService:
    return AssinaturaService(InMemoryAssinaturaRepository(), usinas)


@pytest.fixture
def usina_ativa(usinas: InMemoryUsinaRepository):
    return UsinaService(usinas).criar(
        UsinaCreate(nome="Usina Solar Janauba", localizacao="Janauba, MG", capacidade_geracao_kwh=7800)
    )


def test_criar_assinatura_em_usina_ativa(service, usina_ativa):
    assinatura = service.criar(
        AssinaturaCreate(
            assinante_nome="Padaria Pao de Queijo",
            kwh_contratados=850,
            usina_id=usina_ativa.id,
        )
    )
    assert assinatura.id == 1
    assert assinatura.usina_id == usina_ativa.id


def test_criar_assinatura_em_usina_inexistente_levanta_404(service):
    with pytest.raises(ErroDeNegocio) as erro:
        service.criar(
            AssinaturaCreate(assinante_nome="Padaria Pao de Queijo", kwh_contratados=850, usina_id=99)
        )
    assert erro.value.code == "RECURSO_NAO_ENCONTRADO"
    assert erro.value.status == 404


def test_criar_assinatura_em_usina_inativa_levanta_409(service, usinas, usina_ativa):
    UsinaService(usinas).atualizar(usina_ativa.id, UsinaUpdate(status=StatusUsina.inativa))
    with pytest.raises(ErroDeNegocio) as erro:
        service.criar(
            AssinaturaCreate(
                assinante_nome="Padaria Pao de Queijo",
                kwh_contratados=850,
                usina_id=usina_ativa.id,
            )
        )
    assert erro.value.code == "USINA_INATIVA"
    assert erro.value.status == 409
