import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/matriculas.feature')

BASE_URL = "http://localhost:5001"


@given("existe um projeto publicado disponível para nova matrícula")
def projeto_publicado_para_matricula(context, headers_professor):
    response = requests.post(f"{BASE_URL}/projetos", headers=headers_professor, json={
        "titulo": "Projeto para teste de matrícula",
        "descricao": "Criado automaticamente durante testes",
        "nivel": "iniciante"
    })
    assert response.status_code == 201, f"Falha ao criar projeto: {response.text}"
    projeto_id = response.json()["projeto"]["id"]

    response = requests.post(
        f"{BASE_URL}/projetos/{projeto_id}/etapas",
        headers=headers_professor,
        json={
            "titulo": "Etapa de teste",
            "instrucao": "Instrução para teste automatizado",
            "ordem": 1
        }
    )
    assert response.status_code == 201, f"Falha ao criar etapa: {response.text}"

    response = requests.patch(
        f"{BASE_URL}/projetos/{projeto_id}/publicar",
        headers=headers_professor
    )
    assert response.status_code == 200, f"Falha ao publicar projeto: {response.text}"

    context['projeto_id'] = projeto_id


@given("eu já estou matriculada nesse projeto")
def ja_matriculada(context, headers_estudante):
    response = requests.post(
        f"{BASE_URL}/matriculas",
        headers=headers_estudante,
        json={"projeto_id": context['projeto_id']}
    )
    assert response.status_code == 201, f"Falha ao criar matrícula: {response.text}"


@when("eu me matriculo nesse projeto")
def matricular_projeto(context):
    context['response'] = requests.post(
        f"{BASE_URL}/matriculas",
        headers=context['headers'],
        json={"projeto_id": context['projeto_id']}
    )


@then(parsers.parse('a resposta deve conter o campo "matricula"'))
def verificar_campo_matricula(context):
    body = context['response'].json()
    assert "matricula" in body, f"Campo 'matricula' não encontrado: {body}"