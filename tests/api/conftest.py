import pytest
import requests

BASE_URL = "http://localhost:5001"


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