import pytest
import requests
from pytest_bdd import given, then, parsers

BASE_URL = "http://localhost:5001"


@pytest.fixture
def context():
    return {}


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def token_professor():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "manu@email.com",
        "senha": "123456"
    })
    assert response.status_code == 200, "Falha ao autenticar como professor(a)"
    return response.json()["token"]


@pytest.fixture(scope="session")
def token_estudante():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "lua@email.com",
        "senha": "123456"
    })
    assert response.status_code == 200, "Falha ao autenticar como estudante"
    return response.json()["token"]


@pytest.fixture(scope="session")
def headers_professor(token_professor):
    return {"Authorization": f"Bearer {token_professor}"}


@pytest.fixture(scope="session")
def headers_estudante(token_estudante):
    return {"Authorization": f"Bearer {token_estudante}"}


@given("que a API está rodando")
def api_rodando():
    pass


@given("que estou autenticada como professor(a)")
def autenticada_como_professora(context, headers_professor):
    context["headers"] = dict(headers_professor)


@given("que estou autenticada como estudante")
def autenticada_como_estudante(context, headers_estudante):
    context["headers"] = dict(headers_estudante)


@then(parsers.parse("a resposta deve ter status {status:d}"))
def verificar_status(context, status):
    assert context["response"].status_code == status, (
        f"Esperado {status}, obtido {context['response'].status_code}. "
        f"Resposta: {context['response'].text}"
    )


@then(parsers.parse('a resposta deve conter erro "{mensagem}"'))
def verificar_erro(context, mensagem):
    body = context["response"].json()
    assert "erro" in body, f"Campo 'erro' não encontrado na resposta: {body}"
    assert body["erro"] == mensagem, (
        f"Esperado '{mensagem}', obtido '{body['erro']}'"
    )