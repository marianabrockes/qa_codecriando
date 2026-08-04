import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/submissoes.feature')

BASE_URL = "http://localhost:5001"


def _criar_projeto_publicado(headers_professor):
    response = requests.post(f"{BASE_URL}/projetos", headers=headers_professor, json={
        "titulo": "Projeto para teste de submissão",
        "descricao": "Criado automaticamente durante testes",
        "nivel": "iniciante"
    })
    assert response.status_code == 201, f"Falha ao criar projeto: {response.text}"
    projeto_id = response.json()["projeto"]["id"]

    response = requests.post(
        f"{BASE_URL}/projetos/{projeto_id}/etapas",
        headers=headers_professor,
        json={
            "titulo": "Etapa 1 de teste",
            "instrucao": "Instrução para teste automatizado",
            "ordem": 1
        }
    )
    assert response.status_code == 201, f"Falha ao criar etapa: {response.text}"
    etapa_id = response.json()["etapa"]["id"]

    response = requests.patch(
        f"{BASE_URL}/projetos/{projeto_id}/publicar",
        headers=headers_professor
    )
    assert response.status_code == 200, f"Falha ao publicar projeto: {response.text}"

    return projeto_id, etapa_id


@given("existe uma matrícula em projeto com duas etapas")
def matricula_projeto_duas_etapas(context, headers_professor, headers_estudante):
    response = requests.post(f"{BASE_URL}/projetos", headers=headers_professor, json={
        "titulo": "Projeto com duas etapas para teste",
        "descricao": "Criado automaticamente durante testes",
        "nivel": "iniciante"
    })
    assert response.status_code == 201
    projeto_id = response.json()["projeto"]["id"]

    for ordem, titulo in [(1, "Etapa 1"), (2, "Etapa 2")]:
        response = requests.post(
            f"{BASE_URL}/projetos/{projeto_id}/etapas",
            headers=headers_professor,
            json={"titulo": titulo, "instrucao": f"Instrução da {titulo}", "ordem": ordem}
        )
        assert response.status_code == 201
        if ordem == 2:
            etapa2_id = response.json()["etapa"]["id"]

    response = requests.patch(
        f"{BASE_URL}/projetos/{projeto_id}/publicar",
        headers=headers_professor
    )
    assert response.status_code == 200

    response = requests.post(
        f"{BASE_URL}/matriculas",
        headers=headers_estudante,
        json={"projeto_id": projeto_id}
    )
    assert response.status_code == 201
    matricula_id = response.json()["matricula"]["id"]

    context["matricula_id"] = matricula_id
    context["etapa2_id"] = etapa2_id


@given("existe uma submissão pendente")
def submissao_pendente(context, headers_professor, headers_estudante):
    projeto_id, etapa_id = _criar_projeto_publicado(headers_professor)

    response = requests.post(
        f"{BASE_URL}/matriculas",
        headers=headers_estudante,
        json={"projeto_id": projeto_id}
    )
    assert response.status_code == 201
    matricula_id = response.json()["matricula"]["id"]

    response = requests.post(f"{BASE_URL}/submissoes", headers=headers_estudante, json={
        "matricula_id": matricula_id,
        "etapa_id": etapa_id,
        "conteudo": "Solução automática para teste"
    })
    assert response.status_code == 201, f"Falha ao criar submissão: {response.text}"
    context["submissao_id"] = response.json()["submissao"]["id"]


@when("eu tento submeter a segunda etapa sem aprovar a primeira")
def submeter_segunda_etapa(context, headers_estudante):
    context["response"] = requests.post(f"{BASE_URL}/submissoes", headers=headers_estudante, json={
        "matricula_id": context["matricula_id"],
        "etapa_id": context["etapa2_id"],
        "conteudo": "Tentativa de pular etapa"
    })


@when("eu tento avaliar essa submissão como estudante")
def estudante_avaliar(context, headers_estudante):
    context["response"] = requests.patch(
        f"{BASE_URL}/submissoes/{context['submissao_id']}/avaliar",
        headers=headers_estudante,
        json={"status": "aprovado"}
    )


@when("eu avalio essa submissão com status inválido")
def avaliar_status_invalido(context):
    context["response"] = requests.patch(
        f"{BASE_URL}/submissoes/{context['submissao_id']}/avaliar",
        headers=context["headers"],
        json={"status": "talvez"}
    )


@when("eu aprovo essa submissão com feedback")
def aprovar_submissao(context):
    context["response"] = requests.patch(
        f"{BASE_URL}/submissoes/{context['submissao_id']}/avaliar",
        headers=context["headers"],
        json={"status": "aprovado", "feedback": "Muito bem! Solução correta."}
    )


@when("eu reprovo essa submissão com feedback")
def reprovar_submissao(context):
    context["response"] = requests.patch(
        f"{BASE_URL}/submissoes/{context['submissao_id']}/avaliar",
        headers=context["headers"],
        json={"status": "reprovado", "feedback": "Revise e tente novamente."}
    )


@then(parsers.parse('a submissão deve ter status "{status_submissao}"'))
def verificar_status_submissao(context, status_submissao):
    body = context["response"].json()
    submissao = body.get("submissao", {})
    assert submissao.get("status") == status_submissao, (
        f"Esperado '{status_submissao}', obtido '{submissao.get('status')}'"
    )