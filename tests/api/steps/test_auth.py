import requests
from pytest_bdd import scenarios, when, then, parsers

scenarios('../features/auth.feature')

BASE_URL = "http://localhost:5001"


@when('eu envio POST para "/login" com credenciais válidas da professora')
def login_valido(context):
    context['response'] = requests.post(f"{BASE_URL}/login", json={
        "email": "manu@email.com",
        "senha": "123456"
    })


@when('eu envio POST para "/login" com senha incorreta')
def login_senha_incorreta(context):
    context['response'] = requests.post(f"{BASE_URL}/login", json={
        "email": "manu@email.com",
        "senha": "senhaerrada"
    })


@when('eu envio POST para "/login" com email não cadastrado')
def login_email_invalido(context):
    context['response'] = requests.post(f"{BASE_URL}/login", json={
        "email": "naoexiste@email.com",
        "senha": "123456"
    })


@when('eu envio GET para "/projetos" sem token')
def get_projetos_sem_token(context):
    context['response'] = requests.get(f"{BASE_URL}/projetos")


@when('eu envio POST para "/register" com email já cadastrado')
def register_email_duplicado(context):
    context['response'] = requests.post(f"{BASE_URL}/register", json={
        "nome": "Manu Duplicada",
        "email": "manu@email.com",
        "senha": "123456",
        "perfil": "professor"
    })


@when('eu envio POST para "/register" sem campos obrigatórios')
def register_sem_campos(context):
    context['response'] = requests.post(f"{BASE_URL}/register", json={
        "nome": "Teste Incompleto"
    })


@when('eu envio POST para "/register" com perfil inválido')
def register_perfil_invalido(context):
    context['response'] = requests.post(f"{BASE_URL}/register", json={
        "nome": "Teste",
        "email": "teste_perfil@email.com",
        "senha": "123456",
        "perfil": "administrador"
    })


@when('eu envio POST para "/register" sem corpo')
def register_sem_corpo(context):
    context['response'] = requests.post(
        f"{BASE_URL}/register",
        headers={"Content-Type": "application/json"},
        data=""
    )


@then(parsers.parse('a resposta deve conter o campo "token"'))
def verificar_token(context):
    assert "token" in context['response'].json(), (
        f"Campo 'token' não encontrado: {context['response'].json()}"
    )