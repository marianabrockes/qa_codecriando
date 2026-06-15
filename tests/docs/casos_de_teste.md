# Casos de Teste — CodeCriando

## F01 — Cadastro de pessoa usuária

### CT-001 — Cadastro com dados válidos (professor(a))

**História:** US-01  
**Prioridade:** Alta  
**Pré-condição:** API rodando. Email não cadastrado anteriormente.  
**Dados de teste:**

```json
{
  "nome": "Manu Silva",
  "email": "manu@email.com",
  "senha": "123456",
  "perfil": "professor"
}
```

**Passos:**

1. Enviar POST para `/register` com os dados acima.

**Resultado esperado:** Status 201. Corpo da resposta contém `mensagem` e objeto `usuario` com os dados cadastrados sem o campo `senha`.  
**Resultado obtido:**  
**Status:**

---

### CT-002 — Cadastro com dados válidos (estudante)

**História:** US-01  
**Prioridade:** Alta  
**Pré-condição:** API rodando. Email não cadastrado anteriormente.  
**Dados de teste:**

```json
{
  "nome": "Lua Santos",
  "email": "lua@email.com",
  "senha": "123456",
  "perfil": "estudante"
}
```

**Passos:**

1. Enviar POST para `/register` com os dados acima.

**Resultado esperado:** Status 201. Corpo da resposta contém `mensagem` e objeto `usuario`.  
**Resultado obtido:**  
**Status:**

---

### CT-003 — Cadastro com email já existente

**História:** US-01  
**Prioridade:** Alta  
**Pré-condição:** Email `manu@email.com` já cadastrado (CT-001 executado).  
**Dados de teste:**

```json
{
  "nome": "Manu Duplicada",
  "email": "manu@email.com",
  "senha": "123456",
  "perfil": "professor"
}
```

**Passos:**

1. Enviar POST para `/register` com email já cadastrado.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando que o email já está cadastrado.  
**Resultado obtido:**  
**Status:**

---

### CT-004 — Cadastro sem campos obrigatórios

**História:** US-01  
**Prioridade:** Alta  
**Pré-condição:** API rodando.  
**Dados de teste:**

```json
{
  "nome": "Manu Silva",
  "email": "manu2@email.com"
}
```

**Passos:**

1. Enviar POST para `/register` sem os campos `senha` e `perfil`.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando campos obrigatórios.  
**Resultado obtido:**  
**Status:**

---

### CT-005 — Cadastro com perfil inválido

**História:** US-01  
**Prioridade:** Média  
**Pré-condição:** API rodando.  
**Dados de teste:**

```json
{
  "nome": "Manu Silva",
  "email": "manu3@email.com",
  "senha": "123456",
  "perfil": "administrador"
}
```

**Passos:**

1. Enviar POST para `/register` com perfil inválido.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando os valores aceitos para perfil.  
**Resultado obtido:**  
**Status:**

---

### CT-006 — Cadastro sem corpo na requisição

**História:** US-01  
**Prioridade:** Média  
**Pré-condição:** API rodando.  
**Dados de teste:** Requisição sem corpo.  
**Passos:**

1. Enviar POST para `/register` sem corpo.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro.  
**Resultado obtido:**  
**Status:**

---

## F02 — Login e autenticação JWT

### CT-007 — Login com credenciais válidas

**História:** US-02  
**Prioridade:** Alta  
**Pré-condição:** Pessoa usuária cadastrada com email `manu@email.com` e senha `123456`.  
**Dados de teste:**

```json
{
  "email": "manu@email.com",
  "senha": "123456"
}
```

**Passos:**

1. Enviar POST para `/login` com os dados acima.

**Resultado esperado:** Status 200. Corpo contém `token` JWT e objeto `usuario`.  
**Resultado obtido:**  
**Status:**

---

### CT-008 — Login com senha incorreta

**História:** US-02  
**Prioridade:** Alta  
**Pré-condição:** Pessoa usuária cadastrada com email `manu@email.com`.  
**Dados de teste:**

```json
{
  "email": "manu@email.com",
  "senha": "senhaerrada"
}
```

**Passos:**

1. Enviar POST para `/login` com senha incorreta.

**Resultado esperado:** Status 401. Corpo contém mensagem de erro informando credenciais inválidas.  
**Resultado obtido:**  
**Status:**

---

### CT-009 — Login com email não cadastrado

**História:** US-02  
**Prioridade:** Alta  
**Pré-condição:** API rodando.  
**Dados de teste:**

```json
{
  "email": "naoexiste@email.com",
  "senha": "123456"
}
```

**Passos:**

1. Enviar POST para `/login` com email não cadastrado.

**Resultado esperado:** Status 401. Corpo contém mensagem de erro informando credenciais inválidas.  
**Resultado obtido:**  
**Status:**

---

### CT-010 — Acesso a rota protegida sem token

**História:** US-02  
**Prioridade:** Alta  
**Pré-condição:** API rodando.  
**Dados de teste:** Requisição sem cabeçalho Authorization.  
**Passos:**

1. Enviar GET para `/projetos` sem token JWT.

**Resultado esperado:** Status 401.  
**Resultado obtido:**  
**Status:**

---

## F03 — Criar projeto

### CT-011 — Criar projeto com dados válidos

**História:** US-03  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como professora com token válido.  
**Dados de teste:**

```json
{
  "titulo": "Minha primeira página web",
  "descricao": "Aprenda a criar uma página HTML do zero",
  "nivel": "iniciante"
}
```

**Passos:**

1. Enviar POST para `/projetos` com token da professora e os dados acima.

**Resultado esperado:** Status 201. Projeto criado com status `rascunho`.  
**Resultado obtido:**  
**Status:**

---

### CT-012 — Criar projeto como estudante

**História:** US-03  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como estudante com token válido.  
**Dados de teste:**

```json
{
  "titulo": "Projeto indevido",
  "descricao": "Tentativa de criar projeto como estudante",
  "nivel": "iniciante"
}
```

**Passos:**

1. Enviar POST para `/projetos` com token da estudante.

**Resultado esperado:** Status 403. Corpo contém mensagem de erro.  
**Resultado obtido:**  
**Status:**

---

### CT-013 — Criar projeto sem campos obrigatórios

**História:** US-03  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como professora com token válido.  
**Dados de teste:**

```json
{
  "titulo": "Projeto incompleto"
}
```

**Passos:**

1. Enviar POST para `/projetos` sem `descricao` e `nivel`.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro.  
**Resultado obtido:**  
**Status:**

---

## F04 — Publicar projeto

### CT-014 — Publicar projeto com etapas

**História:** US-04  
**Prioridade:** Alta  
**Pré-condição:** Projeto em rascunho com pelo menos uma etapa criada.  
**Passos:**

1. Enviar PATCH para `/projetos/{projeto_id}/publicar` com token da professora.

**Resultado esperado:** Status 200. Status do projeto muda para `publicado`.  
**Resultado obtido:**  
**Status:**

---

### CT-015 — Publicar projeto sem etapas

**História:** US-04  
**Prioridade:** Alta  
**Pré-condição:** Projeto em rascunho sem etapas.  
**Passos:**

1. Enviar PATCH para `/projetos/{projeto_id}/publicar` com token da professora.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando que o projeto precisa ter pelo menos uma etapa.  
**Resultado obtido:**  
**Status:**

---

### CT-016 — Publicar projeto já publicado

**História:** US-04  
**Prioridade:** Média  
**Pré-condição:** Projeto já com status `publicado`.  
**Passos:**

1. Enviar PATCH para `/projetos/{projeto_id}/publicar` com token da professora.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro.  
**Resultado obtido:**  
**Status:**

---

## F10 — Matricular em projeto

### CT-017 — Matricular em projeto publicado

**História:** US-09  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como estudante. Projeto publicado disponível.  
**Dados de teste:**

```json
{
  "projeto_id": 1
}
```

**Passos:**

1. Enviar POST para `/matriculas` com token da estudante.

**Resultado esperado:** Status 201. Matrícula criada com sucesso.  
**Resultado obtido:**  
**Status:**

---

### CT-018 — Matricular duas vezes no mesmo projeto

**História:** US-09  
**Prioridade:** Alta  
**Pré-condição:** Estudante já matriculada no projeto.  
**Dados de teste:**

```json
{
  "projeto_id": 1
}
```

**Passos:**

1. Enviar POST para `/matriculas` com token da estudante no mesmo projeto.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando que já está matriculada.  
**Resultado obtido:**  
**Status:**

---

### CT-019 — Professora tentando se matricular

**História:** US-09  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como professora.  
**Dados de teste:**

```json
{
  "projeto_id": 1
}
```

**Passos:**

1. Enviar POST para `/matriculas` com token da professora.

**Resultado esperado:** Status 403. Corpo contém mensagem de erro.  
**Resultado obtido:**  
**Status:**

---

## F12 — Submeter etapa

### CT-020 — Submeter primeira etapa

**História:** US-11  
**Prioridade:** Alta  
**Pré-condição:** Estudante matriculada no projeto. Etapa 1 disponível.  
**Dados de teste:**

```json
{
  "matricula_id": 1,
  "etapa_id": 1,
  "conteudo": "Minha solução para a etapa 1"
}
```

**Passos:**

1. Enviar POST para `/submissoes` com token da estudante.

**Resultado esperado:** Status 201. Submissão criada com status `pendente`.  
**Resultado obtido:**  
**Status:**

---

### CT-021 — Submeter etapa 2 sem etapa 1 aprovada

**História:** US-11  
**Prioridade:** Alta  
**Pré-condição:** Estudante matriculada. Etapa 1 com status `pendente` ou `reprovado`.  
**Dados de teste:**

```json
{
  "matricula_id": 1,
  "etapa_id": 2,
  "conteudo": "Tentativa de pular etapa"
}
```

**Passos:**

1. Enviar POST para `/submissoes` com token da estudante tentando submeter etapa 2.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando que a etapa anterior precisa ser aprovada.  
**Resultado obtido:**  
**Status:**

---

## F13 — Avaliar submissão

### CT-022 — Aprovar submissão com feedback

**História:** US-12  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como professora do projeto. Submissão com status `pendente` existente.  
**Dados de teste:**

```json
{
  "status": "aprovado",
  "feedback": "Muito bem! Solução correta."
}
```

**Passos:**

1. Enviar PATCH para `/submissoes/{submissao_id}/avaliar` com token da professora.

**Resultado esperado:** Status 200. Status da submissão muda para `aprovado`. Campo `avaliado_em` preenchido.  
**Resultado obtido:**  
**Status:**

---

### CT-023 — Reprovar submissão com feedback

**História:** US-12  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como professora do projeto. Submissão com status `pendente` existente.  
**Dados de teste:**

```json
{
  "status": "reprovado",
  "feedback": "Revise a tag h1 e tente novamente."
}
```

**Passos:**

1. Enviar PATCH para `/submissoes/{submissao_id}/avaliar` com token da professora.

**Resultado esperado:** Status 200. Status da submissão muda para `reprovado`. Feedback salvo.  
**Resultado obtido:**  
**Status:**

---

### CT-024 — Estudante tentando avaliar submissão

**História:** US-12  
**Prioridade:** Alta  
**Pré-condição:** Autenticada como estudante. Submissão existente.  
**Dados de teste:**

```json
{
  "status": "aprovado"
}
```

**Passos:**

1. Enviar PATCH para `/submissoes/{submissao_id}/avaliar` com token da estudante.

**Resultado esperado:** Status 403. Corpo contém mensagem de erro.  
**Resultado obtido:**  
**Status:**

---

### CT-025 — Avaliar com status inválido

**História:** US-12  
**Prioridade:** Média  
**Pré-condição:** Autenticada como professora do projeto.  
**Dados de teste:**

```json
{
  "status": "talvez"
}
```

**Passos:**

1. Enviar PATCH para `/submissoes/{submissao_id}/avaliar` com status inválido.

**Resultado esperado:** Status 400. Corpo contém mensagem de erro informando os valores aceitos.  
**Resultado obtido:**  
**Status:**
