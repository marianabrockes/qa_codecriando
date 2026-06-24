# Relatório de Bugs — CodeCriando

## Identificação

**Projeto:** CodeCriando  
**Versão:** 1.0.0  
**Data:** junho/2026  
**Responsável:** Mariana Brockes  
**Repositório:** github.com/marianabrockes/qa_codecriando

---

## Resumo executivo

Foram executados 25 casos de teste cobrindo as funcionalidades principais da API. Durante a execução, um caso de teste falhou (CT-006), dois bugs foram registrados e uma inconsistência de comportamento foi identificada.

| ID      | Título                                                                               | Severidade | Status                        |
| ------- | ------------------------------------------------------------------------------------ | ---------- | ----------------------------- |
| BUG-001 | Campo `criado_em` retorna com microssegundos em todos os endpoints                   | Baixa      | Aberto                        |
| BUG-002 | POST /register sem corpo retorna HTML com erro interno exposto                       | Média      | Corrigido, aguardando reteste |
| OBS-001 | Inconsistência no campo de erro entre respostas da aplicação e do Flask-JWT-Extended | Baixa      | Aberto                        |

---

## BUG-001

**Título:** Campo `criado_em` retorna com microssegundos em todos os endpoints

**Severidade:** Baixa  
**Prioridade:** Baixa  
**Status:** Aberto  
**Identificado em:** CT-001  
**Data:** junho/2026

### Descrição

O campo `criado_em` retorna o timestamp com precisão de microssegundos em todos os endpoints que incluem esse campo na resposta. O formato exibido é `2026-06-15T18:53:13.703567`, quando o esperado para uma API REST seria `2026-06-15T18:53:13`, sem a fração de segundos.

O problema não impede o funcionamento da API, mas gera inconsistência no formato dos dados retornados e pode causar problemas em clientes que fazem parsing estrito de datas.

**Endpoints afetados:**

- POST /register
- POST /login
- POST /projetos
- POST /projetos/:id/etapas
- POST /matriculas
- POST /submissoes

### Passos para reprodução

1. Enviar POST para `/register` com body válido.
2. Observar o campo `criado_em` na resposta.

### Resultado esperado

```json
"criado_em": "2026-06-15T18:53:13"
```

### Resultado obtido

```json
"criado_em": "2026-06-15T18:53:13.703567"
```

### Causa raiz

O método `to_dict()` dos models utiliza `.isoformat()` diretamente sobre o objeto `datetime` do Python. Quando o objeto contém microssegundos, o `.isoformat()` os inclui na saída por padrão.

### Correção sugerida

Substituir `.isoformat()` por `.isoformat(timespec='seconds')` ou `.strftime('%Y-%m-%dT%H:%M:%S')` nos métodos `to_dict()` de todos os models afetados.

---

## BUG-002

**Título:** POST /register sem corpo retorna HTML com mensagem de erro interna exposta

**Severidade:** Média  
**Prioridade:** Alta  
**Status:** Corrigido, aguardando reteste  
**Identificado em:** CT-006  
**Data:** junho/2026

### Descrição

Ao enviar uma requisição POST para `/register` sem corpo, a API retornava uma resposta em HTML com a mensagem de erro interna do Python: `"Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)"`.

O problema ocorria porque a exceção levantada pelo Flask ao tentar fazer o parse de um JSON ausente não estava sendo tratada, fazendo a resposta padrão de erro do Werkzeug vazar para o cliente no formato HTML.

Esse comportamento tem dois impactos diretos: expõe detalhes da stack interna da aplicação e quebra o contrato da API, que deve sempre responder em JSON.

### Passos para reprodução (comportamento original)

1. Enviar POST para `/register` sem body e sem o header `Content-Type: application/json`.
2. Observar o corpo e o formato da resposta.

### Resultado esperado

Status 400. Corpo em JSON com mensagem de erro padronizada.

### Resultado obtido

Status 400. Corpo em HTML com o conteúdo:

```
Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)
```

### Correção aplicada

Adicionada verificação explícita do corpo da requisição antes de processar os dados, retornando uma resposta JSON padronizada quando nenhum dado é recebido:

```python
dados = request.get_json()

if not dados:
    return jsonify({'erro': 'Nenhum dado enviado'}), 400
```

**Reteste pendente.**

---

## OBS-001

**Título:** Inconsistência no campo de erro entre respostas da aplicação e do Flask-JWT-Extended

**Severidade:** Baixa  
**Prioridade:** Baixa  
**Status:** Aberto  
**Identificado em:** CT-010  
**Data:** junho/2026

### Descrição

A aplicação utiliza o campo `erro` como padrão para todas as mensagens de erro retornadas pelos endpoints. No entanto, erros gerados diretamente pelo Flask-JWT-Extended, como acesso a rota protegida sem token ou com token inválido, utilizam o campo `msg`. A inconsistência foi observada no CT-010, onde a resposta de autenticação retornou um campo diferente do padrão da API.

### Exemplo

Requisição sem token para GET `/projetos`:

```json
{
  "msg": "Missing Authorization Header"
}
```

Resposta de erro da aplicação para credenciais inválidas:

```json
{
  "erro": "Email ou senha incorretos"
}
```

### Impacto

Quem consome a API precisa tratar dois formatos de erro diferentes dependendo da origem da falha, o que aumenta a complexidade do consumo e pode gerar bugs no cliente caso ele assuma que todas as respostas de erro seguem o mesmo padrão.

### Causa raiz

O Flask-JWT-Extended utiliza seu próprio formato de resposta para erros de autenticação, e a aplicação não sobrescreve esse comportamento com handlers personalizados.

### Correção sugerida

Configurar handlers de erro personalizados para os eventos de autenticação JWT, utilizando os decorators disponibilizados pela biblioteca:

```python
@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'erro': 'Token de acesso ausente'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'erro': 'Token de acesso inválido'}), 422
```

Dessa forma, todos os erros da API passam a retornar o campo `erro`, independente da origem.
