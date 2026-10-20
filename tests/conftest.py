"""
Fixtures compartilhadas por todos os arquivos de teste.
O pytest encontra este arquivo sozinho; nao e preciso importa-lo.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.usina_repository import usina_repository
from app.repositories.usuario_repository import usuario_repository


@pytest.fixture(autouse=True)
def limpar_repositorios():
    """
    Roda antes de CADA teste. Zera os repositorios em memoria para que
    um teste nunca dependa do que outro teste deixou para tras.
    """
    usina_repository.__init__()
    usuario_repository.__init__()
    yield


@pytest.fixture
def client() -> TestClient:
    """Cliente HTTP que chama a API sem precisar subir o uvicorn."""
    return TestClient(app)


def _headers_para(client: TestClient, email: str, senha: str, perfil: str) -> dict:
    client.post(
        "/v1/auth/registrar",
        json={
            "nome": "Operadora Bulbe",
            "email": email,
            "senha": senha,
            "perfil": perfil,
        },
    )
    resposta = client.post(
        "/v1/auth/login",
        data={"username": email, "password": senha},
    )
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def headers_auth(client: TestClient) -> dict:
    """Cadastra um operador, faz login e devolve o cabecalho Authorization."""
    return _headers_para(client, "operacao@bulbe.com.br", "solar12345", "operador")


@pytest.fixture
def headers_admin(client: TestClient) -> dict:
    """Cadastra um administrador, faz login e devolve o cabecalho Authorization."""
    return _headers_para(client, "admin@bulbe.com.br", "solar12345", "administrador")


@pytest.fixture
def usina_valida() -> dict:
    return {
        "nome": "Usina Solar Uberlandia",
        "localizacao": "Uberlandia, MG",
        "capacidade_geracao_kwh": 5000,
    }
