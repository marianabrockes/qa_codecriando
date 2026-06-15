# Plano de Testes — CodeCriando

## 1. Identificação

**Projeto:** CodeCriando  
**Versão:** 1.0.0  
**Data:** junho/2026  
**Responsável:** Mariana Brockes  
**Repositório:** github.com/marianabrockes/qa_codecriando

---

## 2. Objetivo

Validar que a API do CodeCriando atende aos requisitos funcionais definidos nas histórias de usuário, garantindo que as regras de negócio estão implementadas corretamente e que os endpoints respondem conforme esperado em todos os cenários: caminho feliz, erros esperados e casos de borda.

---

## 3. Escopo

### Incluído

- Testes funcionais de todos os endpoints da API REST
- Testes de autenticação e autorização JWT
- Testes de regras de negócio
- Testes de validação de dados de entrada
- Testes de integração entre as entidades
- Testes end to end do frontend
- Testes automatizados de API com PyTest e pytest-bdd
- Testes automatizados de frontend com Cypress

### Excluído

- Testes de performance e carga
- Testes de segurança avançados
- Testes em navegadores além do Chrome
- Testes em dispositivos móveis

---

## 4. Tipos de teste

| Tipo                        | Ferramenta          | Objetivo                                            |
| --------------------------- | ------------------- | --------------------------------------------------- |
| Testes manuais de API       | Postman             | Validar endpoints manualmente                       |
| Testes automatizados de API | PyTest + pytest-bdd | Automatizar cenários críticos                       |
| Testes end to end           | Cypress             | Validar fluxos completos no frontend                |
| Testes de regressão         | PyTest + Cypress    | Garantir que novas mudanças não quebram o existente |

---

## 5. Funcionalidades a testar

| ID  | Funcionalidade                 | Prioridade |
| --- | ------------------------------ | ---------- |
| F01 | Cadastro de pessoa usuária     | Alta       |
| F02 | Login e autenticação JWT       | Alta       |
| F03 | Criar projeto                  | Alta       |
| F04 | Publicar projeto               | Alta       |
| F05 | Editar projeto                 | Média      |
| F06 | Deletar projeto                | Média      |
| F07 | Criar etapa                    | Alta       |
| F08 | Editar etapa                   | Média      |
| F09 | Deletar etapa                  | Média      |
| F10 | Matricular em projeto          | Alta       |
| F11 | Cancelar matrícula             | Média      |
| F12 | Submeter etapa                 | Alta       |
| F13 | Avaliar submissão              | Alta       |
| F14 | Listar projetos publicados     | Média      |
| F15 | Listar matrículas da estudante | Média      |
| F16 | Listar submissões do projeto   | Média      |

---

## 6. Critérios de entrada

- API rodando e acessível em `http://localhost:5001`
- Banco de dados PostgreSQL inicializado e conectado
- Swagger disponível em `http://localhost:5001/apidocs`
- Coleção Postman configurada com variáveis de ambiente
- Ambiente Docker rodando corretamente

---

## 7. Critérios de saída

- Todos os casos de teste de prioridade alta executados
- Taxa de aprovação mínima de 90% nos casos de teste
- Todos os bugs de severidade crítica e alta corrigidos e retestados
- Coleção Postman exportada no repositório
- Relatório de testes gerado

---

## 8. Riscos

| Risco                                 | Probabilidade | Impacto | Mitigação                                     |
| ------------------------------------- | ------------- | ------- | --------------------------------------------- |
| Problema de conexão entre API e banco | Baixa         | Alto    | Docker Compose garante ordem de inicialização |
| Token JWT expirado durante os testes  | Média         | Baixo   | Reconfigurar token no Postman                 |
| Dados de teste inconsistentes         | Média         | Médio   | Limpar banco antes de cada ciclo de testes    |

---

## 9. Ambiente de teste

- **Sistema operacional:** macOS
- **Banco de dados:** PostgreSQL 15 via Docker
- **API:** Flask rodando na porta 5001 via Docker
- **Ferramenta de API:** Postman
- **Automação de API:** PyTest 9.x + pytest-bdd 8.x
- **Automação de frontend:** Cypress
- **CI/CD:** GitHub Actions

---

## 10. Cronograma

| Etapa | Atividade                              |
| ----- | -------------------------------------- |
| 1     | Histórias de usuário e plano de testes |
| 2     | Escrita dos casos de teste             |
| 3     | Testes manuais no Postman              |
| 4     | Documentação de bugs                   |
| 5     | Desenvolvimento do frontend            |
| 6     | Automação com PyTest e pytest-bdd      |
| 7     | Testes E2E com Cypress                 |
| 8     | Relatório final                        |
