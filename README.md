# CodeCriando

**A full-stack EdTech platform built as a working environment for a complete QA cycle and for API troubleshooting and support documentation.**

CodeCriando is a platform where teachers create guided programming projects for children. Projects are organized into sequential stages, and each stage requires a submission that gets reviewed and approved before the student can move on. The business rules are real and enforced: you can't publish a project without stages, you can't skip a stage, you can't delete a project with active enrollments.

I built the platform so I'd have something real to test, break, diagnose, and fix. The result covers two connected tracks: a full QA cycle from requirements through automated regression, and the support documentation a team would actually reach for when something goes wrong.

---

## At a glance

|                          |                                                             |
| ------------------------ | ----------------------------------------------------------- |
| **12 user stories**      | 5 epics, acceptance criteria in Given/When/Then             |
| **25 manual test cases** | Executed in Postman: happy path, error handling, edge cases |
| **43 automated tests**   | 22 API (pytest-bdd) + 21 E2E (Cypress), all passing in CI   |
| **10 SQL queries**       | Data integrity validation directly in PostgreSQL            |
| **3 defects**            | Found, documented with root cause, fixed, and retested      |
| **4 support documents**  | Error reference, runbook, incident report, Postman guide    |
| **CI pipeline**          | GitHub Actions running both suites on every push            |

---

## QA cycle

**Requirements** — [12 user stories](tests/docs/historias_de_usuario.md) across 5 epics (authentication, projects, stages, enrollments, submissions), each with acceptance criteria written in Given/When/Then format.

**Test planning** — A [formal test plan](tests/docs/plano_de_testes.md) defining scope and exclusions, test types and tools, the 16 features under test with priority, entry and exit criteria, risk analysis with mitigations, and the test environment.

**Manual execution** — [25 test cases](tests/docs/casos_de_teste.md) executed by hand in Postman, organized by feature. Each one documents preconditions, test data, steps, expected result, and actual result. Coverage includes the happy path, expected errors (400, 401, 403, 404), permission boundaries between roles, and edge cases like empty request bodies and out-of-order submissions. The [Postman collection](tests/docs/codecriando_api.json) is exported and version-controlled.

**Defect management** — Three issues found during execution, each documented in the [bug report](tests/docs/relatorio_de_bugs.md) with severity, reproduction steps, root cause analysis, and the fix that was actually applied. All three were fixed, retested, and are now covered by automated tests.

**API automation** — 22 tests using pytest-bdd, with Gherkin feature files and step definitions covering authentication, projects, enrollments, and submissions. Every scenario provisions its own data through the API, so the suite runs against a clean database.

**E2E automation** — 21 Cypress tests covering login and logout, the full teacher flow (create project, add stages, publish, evaluate submissions), and the full student flow (browse projects, enroll, submit solutions), including validation of blocked actions.

**Database validation** — [10 SQL queries](tests/docs/queries_sql.md) verifying what the API reported actually landed correctly in PostgreSQL: password hashing, referential integrity, orphaned records, and business rule consistency at the persistence layer.

**Continuous integration** — A [GitHub Actions pipeline](.github/workflows/tests.yml) that provisions PostgreSQL, starts the API, seeds test data, serves the frontend, and runs both test suites on every push.

---

## Support documentation

These are the artifacts I'd want to have if I were the one taking the ticket.

**[Error reference](docs/error-reference.md)** — Every status code and error message the API returns, with the likely cause and the resolution step. Organized by status code so you can go straight from a customer's screenshot to an answer.

**[Troubleshooting runbook](docs/troubleshooting-runbook.md)** — Diagnosis steps for six operational failures: API not responding, database connection errors on startup, blanket 401s, unclear 400s, blocked stage submissions, and undeletable projects. Each one has the commands or SQL to run, the common causes, and a quick-reference table at the end.

**[Incident report](docs/incident-report-bug-002.md)** — A full write-up of the most serious defect found: an endpoint returning raw HTML with an internal Python error exposed. Covers the reported symptom, observed behavior, reproduction steps, root cause, the fix, verification, and what would prevent it from recurring.

**[Postman guide](docs/postman-guide.md)** — How to set up the collection, configure the environment, populate tokens, and deliberately reproduce each documented error scenario.

**Structured logging** — The application logs every request with its status code, and flags authentication failures with context (missing token, expired token, invalid token) so problems can be diagnosed from logs rather than reproduced by hand.

---

## Defects found

| ID      | Issue                                                           | Severity | Root cause                                                     |
| ------- | --------------------------------------------------------------- | -------- | -------------------------------------------------------------- |
| BUG-001 | Timestamps returned with microseconds on every endpoint         | Low      | `.isoformat()` includes microseconds by default                |
| BUG-002 | Empty request body returned HTML with an internal error exposed | Medium   | Unhandled Flask exception bypassed the app's JSON error path   |
| OBS-001 | Auth errors used `msg` while every other error used `erro`      | Low      | Flask-JWT-Extended's default response format wasn't overridden |

**A note on BUG-002:** the fix that seemed obvious wasn't the one that worked. Adding a null check after `request.get_json()` looked correct, but the exception was raised inside `get_json()` before the check ever ran. The actual fix was `get_json(silent=True)`, which returns `None` instead of raising, letting the guard do its job. Retesting is what surfaced that.

---

## What the CI pipeline caught

Two API tests passed locally and failed on the first CI run. Both depended on specific project IDs that existed in my local database but not in the clean one CI creates from scratch.

That's a real defect in the tests, not a CI quirk — a suite that only passes on one machine isn't a regression suite. The fix was making every scenario provision its own data through the API before asserting anything. Worth noting because it's the kind of thing that stays invisible until something forces a clean environment.

---

## Running locally

**Requirements:** Docker, Docker Compose, Python 3.11, Node.js

```bash
git clone https://github.com/marianabrockes/qa_codecriando.git
cd qa_codecriando

cp backend/.env.example backend/.env
# set DATABASE_URL and JWT_SECRET_KEY

docker compose up
```

API at `http://localhost:5001` and Swagger at `http://localhost:5001/apidocs`

**Frontend** (separate terminal):

```bash
cd frontend && python3 -m http.server 8080
```

**API tests:**

```bash
python -m pytest tests/api/ -v
```

**E2E tests** (API and frontend must be running):

```bash
cd tests/e2e && npx cypress run
```

Stuck? The [troubleshooting runbook](docs/troubleshooting-runbook.md) covers the common failures.

---

## Stack

**Backend** — Python, Flask, PostgreSQL, SQLAlchemy, JWT, Flasgger, structured logging

**Frontend** — HTML, CSS, JavaScript (no framework)

**Testing** — Postman, pytest-bdd, Cypress, SQL

**Infrastructure** — Docker, Docker Compose, GitHub Actions

---

## API

18 endpoints across 5 domains. Full error documentation in the [error reference](docs/error-reference.md).

| Domain      | Endpoints                                                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Auth        | `POST /register` · `POST /login`                                                                                                             |
| Projects    | `POST /projetos` · `GET /projetos` · `GET /projetos/<id>` · `PUT /projetos/<id>` · `DELETE /projetos/<id>` · `PATCH /projetos/<id>/publicar` |
| Stages      | `POST /projetos/<id>/etapas` · `PUT /etapas/<id>` · `DELETE /etapas/<id>`                                                                    |
| Enrollments | `POST /matriculas` · `GET /matriculas` · `DELETE /matriculas/<id>`                                                                           |
| Submissions | `POST /submissoes` · `GET /submissoes/<id>` · `PATCH /submissoes/<id>/avaliar` · `GET /projetos/<id>/submissoes`                             |

---

## Repository structure

```
qa_codecriando/
├── .github/workflows/
│   └── tests.yml                   # CI: API + E2E on every push
├── backend/
│   └── app/
│       ├── models/                 # usuario, projeto, etapa, matricula, submissao
│       └── routes/                 # auth, projetos, etapas, matriculas, submissoes
├── frontend/                       # HTML, CSS, JS
├── docs/
│   ├── error-reference.md          # status codes, causes, resolutions
│   ├── troubleshooting-runbook.md  # operational diagnosis
│   ├── incident-report-bug-002.md  # formal incident write-up
│   └── postman-guide.md            # collection setup and error reproduction
└── tests/
    ├── api/
    │   ├── features/               # Gherkin scenarios
    │   └── steps/                  # pytest-bdd step definitions
    ├── e2e/                        # Cypress specs
    └── docs/
        ├── historias_de_usuario.md
        ├── plano_de_testes.md
        ├── casos_de_teste.md
        ├── relatorio_de_bugs.md
        ├── queries_sql.md
        └── codecriando_api.json    # exported Postman collection
```

---

Built by [Mariana Brockes](https://linkedin.com/in/marianabrockes).
