# CodeCriando: QA & Testing

CodeCriando is an EdTech platform where teachers create guided programming projects for children: projects are organized into sequential stages, and each stage requires a submission that gets reviewed and approved before the student can move on.

This repository is the one that best represents how I approach QA and support work. The goal here was never just to prove the API works, but to run a real testing cycle: write user stories with clear acceptance criteria, plan what and how to test, execute and document every case by hand, and when something breaks, document it the way a support or QA engineer would, with enough detail for anyone to reproduce it, understand the root cause, and confirm the fix.

---

## What's in this repository

- **Backend**: Flask API with JWT authentication and PostgreSQL, covering user registration and login, project creation and publishing, stage management, student enrollment, and submission review. 18 REST endpoints across 5 domains, documented via Swagger.
- **User Stories**: 12 user stories across 5 epics (`historias_de_usuario.md`), each with acceptance criteria written in DADO/QUANDO/ENTAO (Given/When/Then) format.
- **Test Plan**: formal test plan covering scope, test types, entry and exit criteria, risks, and schedule (`plano_de_testes.md`).
- **Manual Testing**: 25 test cases executed by hand in Postman (`casos_de_teste.md`), covering the happy path, expected errors, and edge cases for every user story, each documented with test data, steps, expected result, and actual result.
- **Bug Report**: 2 real bugs and 1 behavior inconsistency found during testing (`relatorio_de_bugs.md`), each with severity, reproduction steps, root cause analysis, and the fix that was actually applied to the code.
- **Postman Collection**: exported collection with 35 requests covering the full API (`codecriando_api.json`).

---

## Personas

**Manu (teacher)**: creates guided programming projects, adds stages, publishes projects, and reviews student submissions.

**Lua (student)**: enrolls in published projects, submits solutions for each stage, and needs the previous stage approved before submitting the next one.

---

## Bugs found

| ID      | Title                                                                                 | Severity | Status             |
| ------- | ------------------------------------------------------------------------------------- | -------- | ------------------ |
| BUG-001 | `criado_em` field returns timestamps with microseconds on every endpoint              | Low      | Fixed and retested |
| BUG-002 | `POST /register` without a body returns raw HTML with an internal error exposed       | Medium   | Fixed and retested |
| OBS-001 | Inconsistent error field between the app's own errors and Flask-JWT-Extended's errors | Low      | Fixed and retested |

Full reproduction steps, root cause, and applied fix for each one are in `tests/docs/relatorio_de_bugs.md`.

---

## API Endpoints

| Domain      | Method | Route                               |
| ----------- | ------ | ----------------------------------- |
| Auth        | POST   | `/register`                         |
| Auth        | POST   | `/login`                            |
| Projects    | POST   | `/projetos`                         |
| Projects    | GET    | `/projetos`                         |
| Projects    | GET    | `/projetos/<id>`                    |
| Projects    | PUT    | `/projetos/<id>`                    |
| Projects    | DELETE | `/projetos/<id>`                    |
| Projects    | PATCH  | `/projetos/<id>/publicar`           |
| Stages      | POST   | `/projetos/<projeto_id>/etapas`     |
| Stages      | PUT    | `/etapas/<id>`                      |
| Stages      | DELETE | `/etapas/<id>`                      |
| Enrollments | POST   | `/matriculas`                       |
| Enrollments | GET    | `/matriculas`                       |
| Enrollments | DELETE | `/matriculas/<id>`                  |
| Submissions | POST   | `/submissoes`                       |
| Submissions | GET    | `/submissoes/<id>`                  |
| Submissions | PATCH  | `/submissoes/<id>/avaliar`          |
| Submissions | GET    | `/projetos/<projeto_id>/submissoes` |

---

## Tech Stack

- **Python 3.11 / Flask** - API framework
- **Flask-JWT-Extended** - authentication
- **Flask-SQLAlchemy / PostgreSQL** - data persistence
- **Flasgger** - Swagger documentation
- **Postman** - manual API testing
- **Docker / Docker Compose** - local environment (API + PostgreSQL)

---

## Roadmap

The next step for this project is test automation. `pytest`, `pytest-bdd`, and `gherkin-official` are already set up as dependencies, and the test plan defines the intended coverage, but the automated suite itself is still in progress:

- [ ] Automated API tests with PyTest and pytest-bdd, turning the existing Gherkin-style acceptance criteria into executable scenarios
- [ ] End-to-end frontend tests with Cypress
- [ ] CI pipeline with GitHub Actions to run the suite on every push

---

## Running Locally

**Requirements:** Docker, Docker Compose

```bash
# 1. Clone
git clone https://github.com/marianabrockes/qa_codecriando.git
cd qa_codecriando

# 2. Configure environment variables
cp backend/.env.example backend/.env
# edit backend/.env with your DATABASE_URL and JWT_SECRET_KEY

# 3. Run
docker-compose up
```

API available at `http://localhost:5001`
Swagger docs at `http://localhost:5001/apidocs`

---

## File Structure

```
qa_codecriando/
├── backend/
│   ├── app/
│   │   ├── models/       # usuario, projeto, etapa, matricula, submissao
│   │   └── routes/       # auth, projetos, etapas, matriculas, submissoes
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py
├── tests/
│   └── docs/
│       ├── historias_de_usuario.md
│       ├── plano_de_testes.md
│       ├── casos_de_teste.md
│       ├── relatorio_de_bugs.md
│       └── codecriando_api.json
├── docker-compose.yml
└── README.md
```
