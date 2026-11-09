import os

os.environ["BULBE_DATABASE_URL"] = "sqlite:///./bulbe_test.db"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def banco_limpo():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture(scope="session", autouse=True)
def remover_banco_de_teste():
    yield
    engine.dispose()
    if os.path.exists("bulbe_test.db"):
        os.remove("bulbe_test.db")


@pytest.fixture
def client() -> TestClient:
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
    return _headers_para(client, "operacao@bulbe.com.br", "solar12345", "operador")


@pytest.fixture
def headers_admin(client: TestClient) -> dict:
    return _headers_para(client, "admin@bulbe.com.br", "solar12345", "administrador")


@pytest.fixture
def usina_valida() -> dict:
    return {
        "nome": "Usina Solar Uberlandia",
        "localizacao": "Uberlandia, MG",
        "capacidade_geracao_kwh": 5000,
    }
