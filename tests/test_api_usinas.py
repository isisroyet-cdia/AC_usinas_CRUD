def test_listar_usinas_e_publico(client):
    resposta = client.get("/v1/usinas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_usina_sem_token_retorna_401(client, usina_valida):
    resposta = client.post("/v1/usinas", json=usina_valida)
    assert resposta.status_code == 401
    assert resposta.json()["error"]["code"] == "TOKEN_INVALIDO"


def test_criar_usina_com_token_retorna_201(client, headers_auth, usina_valida):
    resposta = client.post("/v1/usinas", json=usina_valida, headers=headers_auth)
    assert resposta.status_code == 201
    assert resposta.json()["id"] == 1


def test_token_falso_retorna_401(client, usina_valida):
    resposta = client.post(
        "/v1/usinas",
        json=usina_valida,
        headers={"Authorization": "Bearer token.falso.qualquer"},
    )
    assert resposta.status_code == 401


def test_remover_usina_com_token_de_operador_retorna_403(client, headers_auth, usina_valida):
    client.post("/v1/usinas", json=usina_valida, headers=headers_auth)
    client.put("/v1/usinas/1", json={"status": "inativa"}, headers=headers_auth)
    resposta = client.delete("/v1/usinas/1", headers=headers_auth)
    assert resposta.status_code == 403
    assert resposta.json()["error"]["code"] == "ACESSO_NEGADO"


def test_remover_usina_com_token_de_admin(client, headers_admin, usina_valida):
    client.post("/v1/usinas", json=usina_valida, headers=headers_admin)
    client.put("/v1/usinas/1", json={"status": "inativa"}, headers=headers_admin)
    resposta = client.delete("/v1/usinas/1", headers=headers_admin)
    assert resposta.status_code == 204
    assert client.get("/v1/usinas/1").status_code == 404


def test_login_com_senha_errada_retorna_401(client):
    client.post(
        "/v1/auth/registrar",
        json={"nome": "Operadora Bulbe", "email": "operacao@bulbe.com.br", "senha": "solar12345"},
    )
    resposta = client.post(
        "/v1/auth/login",
        data={"username": "operacao@bulbe.com.br", "password": "senhaerrada"},
    )
    assert resposta.status_code == 401
    assert resposta.json()["error"]["code"] == "CREDENCIAIS_INVALIDAS"


def test_rota_me_devolve_o_usuario_logado(client, headers_auth):
    resposta = client.get("/v1/auth/me", headers=headers_auth)
    assert resposta.status_code == 200
    assert resposta.json()["email"] == "operacao@bulbe.com.br"
    assert resposta.json()["perfil"] == "operador"
