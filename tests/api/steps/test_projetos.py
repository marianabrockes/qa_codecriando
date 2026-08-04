import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/projetos.feature')

BASE_URL = "http://localhost:5001"


@given('existe um projeto em rascunho com pelo menos uma etapa')
def projeto_rascunho_com_etapa(context):
    response = requests.post(f"{BASE_URL}/projetos", headers=context['headers'], json={
        "titulo": "Projeto para publicação automática",
        "descricao": "Criado automaticamente durante testes",
        "nivel": "iniciante"
    })
    assert response.status_code == 201, f"Falha ao criar projeto: {response.text}"
    projeto_id = response.json()["projeto"]["id"]
    context['projeto_id'] = projeto_id

    response = requests.post(
        f"{BASE_URL}/projetos/{projeto_id}/etapas",
        headers=context['headers'],
        json={
            "titulo": "Etapa de teste",
            "instrucao": "Instrução para teste automatizado",
            "ordem": 1
        }
    )
    assert response.status_code == 201, f"Falha ao criar etapa: {response.text}"


@when('eu envio POST para "/projetos" com dados válidos')
def criar_projeto(context):
    context['response'] = requests.post(f"{BASE_URL}/projetos", headers=context['headers'], json={
        "titulo": "Projeto de teste automatizado",
        "descricao": "Criado pelo PyTest",
        "nivel": "iniciante"
    })


@when('eu envio POST para "/projetos" sem campos obrigatórios')
def criar_projeto_incompleto(context):
    context['response'] = requests.post(f"{BASE_URL}/projetos", headers=context['headers'], json={
        "titulo": "Projeto incompleto"
    })


@when('eu envio PATCH para publicar o projeto 4')
def publicar_projeto_sem_etapas(context):
    context['response'] = requests.patch(
        f"{BASE_URL}/projetos/4/publicar",
        headers=context['headers']
    )


@when('eu envio PATCH para publicar o projeto 1')
def publicar_projeto_ja_publicado(context):
    context['response'] = requests.patch(
        f"{BASE_URL}/projetos/1/publicar",
        headers=context['headers']
    )


@when('eu publico esse projeto')
def publicar_projeto(context):
    projeto_id = context['projeto_id']
    context['response'] = requests.patch(
        f"{BASE_URL}/projetos/{projeto_id}/publicar",
        headers=context['headers']
    )


@then(parsers.parse('o projeto deve ter status "{status_projeto}"'))
def verificar_status_projeto(context, status_projeto):
    body = context['response'].json()
    projeto = body.get("projeto", {})
    assert projeto.get("status") == status_projeto, (
        f"Esperado '{status_projeto}', obtido '{projeto.get('status')}'"
    )