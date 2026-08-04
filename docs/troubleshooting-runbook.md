# Troubleshooting Runbook — CodeCriando API

## Overview

This runbook covers the most common operational issues encountered when running the CodeCriando API. It is intended for support and operations teams diagnosing problems in local or staging environments.

**Stack:** Python, Flask, PostgreSQL, Docker, JWT
**API port:** 5001
**Database port:** 5432

---

## Issue 1 — API is not responding

**Symptom:** Requests to `http://localhost:5001` time out or return a connection refused error.

**Diagnosis steps:**

1.  Check if the Docker containers are running:

        docker compose ps

    Both `api` and `db` containers should show status `Up`.

2.  If containers are not running, start them:

        docker compose up

3.  If the containers are running but the API is still unreachable, check the API logs for startup errors:

        docker compose logs api

4.  Confirm the API is listening on the correct port:

        curl http://localhost:5001/apidocs

**Common causes:**

- Docker is not running on the host machine.
- Port 5001 is being used by another process.
- The API container exited due to a startup error such as a missing environment variable or a database connection failure.

---

## Issue 2 — Database connection error on startup

**Symptom:** The API container starts but immediately exits. Logs show a database connection error.

**Diagnosis steps:**

1.  Check the API container logs:

        docker compose logs api

    Look for messages containing `could not connect to server` or `connection refused`.

2.  Check if the database container is running and healthy:

        docker compose ps
        docker compose logs db

3.  Restart both containers:

        docker compose down
        docker compose up

4.  Verify the environment variables in `backend/.env` match the database configuration in `docker-compose.yml`. The following variables must be consistent: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and `DATABASE_URL`.

**Common causes:**

- The database container took longer than expected to initialize and the API tried to connect before it was ready.
- A mismatch between the credentials in `.env` and `docker-compose.yml`.

---

## Issue 3 — All authenticated requests return 401

**Symptom:** Requests to protected endpoints return status 401 with the message `Token de acesso expirado` or `Token de acesso ausente`.

**Diagnosis steps:**

1.  If the error is `Token de acesso ausente`, the `Authorization` header is missing from the request. Add the following header to your request:

        Authorization: Bearer <token>

2.  If the error is `Token de acesso expirado`, the JWT token has expired. Tokens are valid for 24 hours. Authenticate again by sending a POST request to `/login` with a valid email and password. Copy the `token` field from the response and use it in subsequent requests.

3.  If the error is `Token de acesso inválido`, the token is malformed or was signed with a different secret key. This can happen after the application is restarted with a different `JWT_SECRET_KEY` in `.env`. Authenticate again to obtain a valid token.

4.  In Postman, update the environment variable `token_professor` or `token_estudante` with the new token value.

**Common causes:**

- Token expired after 24 hours.
- The `Authorization` header was not included in the request.
- The application was restarted with a new JWT secret key, invalidating all existing tokens.

---

## Issue 4 — POST requests return 400 with no clear error message

**Symptom:** A POST request returns status 400 but the response body is empty or unexpected.

**Diagnosis steps:**

1. Verify that the `Content-Type: application/json` header is present in the request.

2. Verify that the request body is valid JSON. An empty body or a body without proper JSON formatting will trigger a 400 response with the message `Nenhum dado enviado`.

3. Check that all required fields are present in the request body. Refer to the API Error Reference in `docs/error-reference.md` for the list of required fields per endpoint.

4. Test the endpoint using the Postman collection included in `tests/docs/codecriando_api.json` to compare with a known working request.

---

## Issue 5 — Student cannot submit a stage

**Symptom:** A POST request to `/submissoes` returns status 400 with the message `A etapa anterior precisa ser aprovada antes de continuar`.

**Diagnosis steps:**

1.  Confirm the student is enrolled in the project:

        SELECT * FROM matriculas WHERE estudante_id = <student_id> AND projeto_id = <project_id>;

2.  Check the status of the previous stage submission:

        SELECT s.status, e.ordem
        FROM submissoes s
        JOIN etapas e ON e.id = s.etapa_id
        WHERE s.matricula_id = <matricula_id>
        ORDER BY e.ordem;

3.  If the previous stage submission has status `pendente` or `reprovado`, it must be approved by the project professor before the student can proceed.

4.  If no submission exists for the previous stage, the student must submit it first.

**Common causes:**

- The student attempted to skip a stage.
- The previous stage submission is still pending evaluation.
- The previous stage submission was reprovado and the student has not resubmitted.

---

## Issue 6 — Cannot delete a project

**Symptom:** A DELETE request to `/projetos/:id` returns status 400 with the message `Não é possível deletar projeto com matrículas ativas`.

**Diagnosis steps:**

1.  Check how many active enrollments the project has:

        SELECT COUNT(*) FROM matriculas WHERE projeto_id = <project_id>;

2.  If enrollments exist, they must be cancelled before the project can be deleted. Each enrollment must be cancelled individually via DELETE /matriculas/:id.

3.  After all enrollments are cancelled, retry the project deletion.

**Common causes:**

- The project has active student enrollments and cannot be deleted while they exist.

---

## Quick Reference

| Symptom                         | First check                                     |
| ------------------------------- | ----------------------------------------------- |
| Connection refused on port 5001 | `docker compose ps`                             |
| API exits on startup            | `docker compose logs api`                       |
| 401 on all requests             | Token expired — re-authenticate via POST /login |
| 400 with no clear message       | Missing Content-Type header or empty body       |
| Cannot submit stage             | Previous stage not approved                     |
| Cannot delete project           | Active enrollments exist                        |
