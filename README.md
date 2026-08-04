# CodeCriando

A portfolio project built to demonstrate hands-on experience in API troubleshooting, bug documentation, and technical support workflows — developed through a complete QA and support cycle on a Flask/PostgreSQL REST API.

CodeCriando is an EdTech platform where teachers create guided programming projects for children. Projects are organized into sequential stages, and each stage requires a submission that gets reviewed and approved before the student can move on.

This repository exists because I wanted a project that would show how I actually work, not just that I know the tools. That means running a real testing cycle: writing user stories with acceptance criteria, planning what to test and why, executing every case by hand, documenting bugs the way a support engineer would, fixing them, and retesting. It also means building the documentation a support team would actually use: an error reference, a troubleshooting runbook, a Postman guide, and a formal incident report.

---

## What this project covers

**QA cycle**

- 12 user stories across 5 epics with DADO/QUANDO/ENTAO acceptance criteria
- Formal test plan covering scope, test types, entry and exit criteria, and risks
- 25 test cases executed manually in Postman, covering happy path, expected errors, and edge cases
- 2 bugs and 1 behavior inconsistency found, documented with severity, reproduction steps, root cause, and applied fix
- 22 automated API tests with PyTest and pytest-bdd, all passing

**Technical support documentation**

- API error reference: every status code and error message the API returns, with causes and resolution steps
- Troubleshooting runbook: step-by-step diagnosis for the most common operational issues
- Postman guide: how to set up the collection, authenticate, and reproduce error scenarios
- Incident report: a formal write-up of BUG-002, from symptom to prevention
- Structured logging on all routes and JWT error handlers

**Backend**

- Flask REST API with JWT authentication and PostgreSQL
- 18 endpoints across 5 domains, documented via Swagger
- Business rules enforced at the API layer: sequential stage progression, enrollment validation, role-based access control

---

## Personas

**Manu (teacher):** creates guided programming projects, adds stages, publishes projects, and reviews student submissions.

**Lua (student):** enrolls in published projects, submits solutions for each stage, and needs the previous stage approved before submitting the next one.

---

## Bugs found and fixed

| ID      | Title                                                                                 | Severity | Status             |
| ------- | ------------------------------------------------------------------------------------- | -------- | ------------------ |
| BUG-001 | `criado_em` field returns timestamps with microseconds on every endpoint              | Low      | Fixed and retested |
| BUG-002 | `POST /register` without a body returns raw HTML with an internal error exposed       | Medium   | Fixed and retested |
| OBS-001 | Inconsistent error field between the app's own errors and Flask-JWT-Extended's errors | Low      | Fixed and retested |

Full reproduction steps, root cause, and applied fix: `tests/docs/relatorio_de_bugs.md`
Formal incident report for BUG-002: `docs/incident-report-bug-002.md`

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

Full error reference for all endpoints: `docs/error-reference.md`

---

## Tech Stack

- **Python 3.11 / Flask** — API framework
- **Flask-JWT-Extended** — authentication
- **Flask-SQLAlchemy / PostgreSQL** — data persistence
- **Flasgger** — Swagger documentation
- **Postman** — manual API testing and collection
- **PyTest / pytest-bdd** — automated API testing
- **Docker / Docker Compose** — local environment

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

# 3. Start the environment
docker compose up
```

API available at `http://localhost:5001`
Swagger docs at `http://localhost:5001/apidocs`

**Running the automated tests:**

```bash
source backend/.venv/bin/activate
python -m pytest tests/api/ -v
```

For troubleshooting the local environment, see `docs/troubleshooting-runbook.md`.

---

## Repository Structure

```
qa_codecriando/
├── backend/
│   ├── app/
│   │   ├── models/         # usuario, projeto, etapa, matricula, submissao
│   │   └── routes/         # auth, projetos, etapas, matriculas, submissoes
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py
├── docs/
│   ├── error-reference.md          # all status codes and error messages
│   ├── incident-report-bug-002.md  # formal incident report
│   ├── postman-guide.md            # collection setup and usage
│   └── troubleshooting-runbook.md  # operational issue diagnosis
├── tests/
│   ├── api/
│   │   ├── features/       # Gherkin scenarios (auth, projetos, matriculas, submissoes)
│   │   └── steps/          # pytest-bdd step definitions and conftest
│   └── docs/
│       ├── historias_de_usuario.md
│       ├── plano_de_testes.md
│       ├── casos_de_teste.md
│       ├── relatorio_de_bugs.md
│       ├── queries_sql.md
│       └── codecriando_api.json
├── docker-compose.yml
└── README.md
```

---

## Roadmap

- [x] User stories and test plan
- [x] 25 manual test cases executed in Postman
- [x] Bug documentation, fixes, and retesting
- [x] 22 automated API tests with PyTest and pytest-bdd
- [x] SQL validation queries
- [x] API error reference
- [x] Troubleshooting runbook
- [x] Incident report
- [x] Structured logging
- [ ] Frontend (HTML/CSS/JS)
- [ ] End-to-end tests with Cypress
- [ ] CI pipeline with GitHub Actions
