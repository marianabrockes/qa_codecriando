# Postman Guide — CodeCriando API

## Overview

This guide explains how to use the Postman collection included in this repository to interact with and troubleshoot the CodeCriando API. It covers environment setup, authentication, and how to reproduce common error scenarios.

**Collection file:** `tests/docs/codecriando_api.json`
**Environment:** CodeCriando - Local

---

## Requirements

- Postman installed (desktop or web)
- Docker running with `docker compose up` from the project root
- API accessible at `http://localhost:5001`

---

## Setup

### 1. Import the collection

1. Open Postman.
2. Click **Import** in the top left.
3. Select the file `tests/docs/codecriando_api.json` from the repository.
4. The collection **CodeCriando API** will appear in your sidebar.

### 2. Configure the environment

The collection uses environment variables to avoid hardcoding values across requests.

1. In Postman, click **Environments** in the left sidebar.
2. Create a new environment named **CodeCriando - Local**.
3. Add the following variables:

| Variable          | Initial value           | Description                         |
| ----------------- | ----------------------- | ----------------------------------- |
| `base_url`        | `http://localhost:5001` | Base URL of the API                 |
| `token_professor` | (empty)                 | JWT token for the professor account |
| `token_estudante` | (empty)                 | JWT token for the student account   |

4. Select **CodeCriando - Local** as the active environment using the dropdown in the top right corner.

### 3. Authenticate and populate tokens

The collection is organized in folders. Start with the **Autenticação** folder.

1. Open the request **CT-007 — Login com credenciais válidas (professor)**.
2. Click **Send**.
3. Copy the value of the `token` field from the response body.
4. Paste it into the `token_professor` environment variable.
5. Repeat the process using the student login request to populate `token_estudante`.

The collection is configured to use `token_professor` as the default Bearer token at the collection level. Requests that require the student token override this at the request level under **Authorization > Bearer Token > token_estudante**.

---

## Collection structure

| Folder       | Contents                                               |
| ------------ | ------------------------------------------------------ |
| Autenticação | Register and login requests, including error scenarios |
| Projetos     | Create, list, edit, publish, and delete projects       |
| Etapas       | Create, edit, and delete project stages                |
| Matrículas   | Enroll, list, and cancel enrollments                   |
| Submissões   | Submit stages and evaluate submissions                 |

---

## Reproducing error scenarios

The collection includes named requests for each test case. To reproduce a specific error:

1. Locate the request by its CT number in the appropriate folder.
2. Verify the request body and headers match the scenario description.
3. Click **Send** and compare the response with the expected result documented in `tests/docs/casos_de_teste.md`.

### Common scenarios

**Empty body returning 400 instead of HTML (BUG-002)**

1.  Open **CT-006 — Cadastro sem corpo na requisição** in the Autenticação folder.
2.  Confirm the Body tab is set to **raw / JSON** with an empty value.
3.  Confirm the Headers tab includes `Content-Type: application/json`.
4.  Send the request. The response should be:

        {
            "erro": "Nenhum dado enviado"
        }

**Token expired returning 401**

1.  Open any request that requires authentication.
2.  Manually replace the Bearer token with an expired or invalid value.
3.  Send the request. The response should be:

        {
            "erro": "Token de acesso expirado"
        }

**Student attempting to create a project (403)**

1.  Open **CT-012 — Criar projeto como estudante** in the Projetos folder.
2.  Verify the Authorization tab is set to use `token_estudante`.
3.  Send the request. The response should be:

        {
            "erro": "Apenas professor(a) pode criar projetos"
        }

---

## Updating tokens after expiration

JWT tokens expire after 24 hours. When a request starts returning 401 with `Token de acesso expirado`:

1. Open the login request for the affected account in the Autenticação folder.
2. Send the request to obtain a new token.
3. Copy the new token value.
4. Open the **CodeCriando - Local** environment.
5. Update the corresponding variable (`token_professor` or `token_estudante`).
6. Save the environment.

All subsequent requests will use the updated token automatically.

---

## Exporting results

To share test results from a collection run:

1. Click the collection name in the sidebar.
2. Select **Run collection**.
3. Configure the run settings and click **Run CodeCriando API**.
4. After the run completes, click **Export Results** to save a JSON report.
