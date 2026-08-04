# API Error Reference — CodeCriando

## Overview

This document lists all error responses returned by the CodeCriando API, including their HTTP status codes, error messages, likely causes, and recommended resolution steps. It is intended for support and integration teams troubleshooting issues with the API.

**Base URL:** `http://localhost:5001`  
**Authentication:** Bearer Token (JWT)  
**Error format:**

```json
{
  "erro": "Error message here"
}
```

---

## 400 Bad Request

Returned when the request is malformed, missing required fields, or violates a business rule.

| Error message                                              | Cause                                                                                    | Resolution                                                                            |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `Todos os campos são obrigatórios`                         | One or more required fields are missing from the request body.                           | Check the request body and include all required fields.                               |
| `Perfil deve ser professor ou estudante`                   | The `perfil` field contains an invalid value.                                            | Use only `professor` or `estudante` as the value for `perfil`.                        |
| `Email já cadastrado`                                      | The provided email address is already registered.                                        | Use a different email address or authenticate with the existing account.              |
| `Nenhum dado enviado`                                      | The request body is empty or the `Content-Type` header is not set to `application/json`. | Include a valid JSON body and set `Content-Type: application/json`.                   |
| `Email e senha são obrigatórios`                           | The login request is missing `email` or `senha`.                                         | Include both fields in the request body.                                              |
| `Não é possível publicar projeto sem etapas`               | A publish request was made for a project with no stages.                                 | Add at least one stage to the project before publishing.                              |
| `Projeto já está publicado`                                | The project is already in `publicado` status.                                            | No action needed. The project is already available for enrollment.                    |
| `Não é possível editar projeto já publicado`               | An edit request was made for a published project.                                        | Published projects cannot be edited. Create a new project if changes are needed.      |
| `Não é possível adicionar etapas em projeto já publicado`  | A stage creation request was made for a published project.                               | Stages can only be added to projects in `rascunho` status.                            |
| `Não é possível editar etapa de projeto já publicado`      | An edit request was made for a stage belonging to a published project.                   | Stages of published projects cannot be modified.                                      |
| `Não é possível deletar etapa de projeto já publicado`     | A delete request was made for a stage belonging to a published project.                  | Stages of published projects cannot be deleted.                                       |
| `Não é possível deletar projeto com matrículas ativas`     | A delete request was made for a project that has active enrollments.                     | Cancel all enrollments before deleting the project.                                   |
| `Não é possível se matricular em projeto não publicado`    | An enrollment request was made for a project in `rascunho` status.                       | Only published projects accept enrollments.                                           |
| `Estudante já matriculada neste projeto`                   | The student is already enrolled in the project.                                          | No action needed. The student is already enrolled.                                    |
| `projeto_id é obrigatório`                                 | The enrollment request body is missing the `projeto_id` field.                           | Include `projeto_id` in the request body.                                             |
| `A etapa anterior precisa ser aprovada antes de continuar` | A submission was made for a stage before the previous stage was approved.                | Wait for the previous stage submission to be approved before submitting the next one. |
| `Status deve ser aprovado ou reprovado`                    | The evaluation request contains an invalid value for `status`.                           | Use only `aprovado` or `reprovado` as the value for `status`.                         |
| `Etapa não pertence ao projeto desta matrícula`            | The submitted stage does not belong to the project the student is enrolled in.           | Verify that the `etapa_id` belongs to the correct project.                            |

---

## 401 Unauthorized

Returned when authentication fails or is missing.

| Error message               | Cause                                                       | Resolution                                                         |
| --------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| `Email ou senha incorretos` | The provided email does not exist or the password is wrong. | Verify the credentials and try again.                              |
| `Token de acesso ausente`   | The request did not include an `Authorization` header.      | Include the header `Authorization: Bearer <token>` in the request. |
| `Token de acesso expirado`  | The JWT token has expired.                                  | Authenticate again via `POST /login` to obtain a new token.        |

---

## 422 Unprocessable Entity

Returned when the JWT token is present but invalid or malformed.

| Error message              | Cause                                                                          | Resolution                                                    |
| -------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| `Token de acesso inválido` | The token is malformed, was tampered with, or was signed with a different key. | Authenticate again via `POST /login` to obtain a valid token. |

---

## 403 Forbidden

Returned when the authenticated user does not have permission to perform the requested action.

| Error message                                       | Cause                                                                                               | Resolution                                                               |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `Apenas professor(a) pode criar projetos`           | A student account attempted to create a project.                                                    | Use a `professor` account to create projects.                            |
| `Apenas estudante pode se matricular em projetos`   | A professor account attempted to enroll in a project.                                               | Use a `estudante` account to enroll in projects.                         |
| `Apenas estudante pode listar matrículas`           | A professor account attempted to list enrollments.                                                  | Use a `estudante` account to list enrollments.                           |
| `Sem permissão para editar este projeto`            | The authenticated professor is not the owner of the project.                                        | Only the professor who created the project can edit it.                  |
| `Sem permissão para publicar este projeto`          | The authenticated professor is not the owner of the project.                                        | Only the professor who created the project can publish it.               |
| `Sem permissão para deletar este projeto`           | The authenticated professor is not the owner of the project.                                        | Only the professor who created the project can delete it.                |
| `Sem permissão para adicionar etapas neste projeto` | The authenticated professor is not the owner of the project.                                        | Only the professor who created the project can add stages.               |
| `Sem permissão para editar esta etapa`              | The authenticated professor is not the owner of the project this stage belongs to.                  | Only the professor who created the project can edit its stages.          |
| `Sem permissão para deletar esta etapa`             | The authenticated professor is not the owner of the project this stage belongs to.                  | Only the professor who created the project can delete its stages.        |
| `Sem permissão para submeter nesta matrícula`       | The authenticated student is not the owner of the enrollment.                                       | Students can only submit to their own enrollments.                       |
| `Sem permissão para avaliar esta submissão`         | The authenticated user is not the professor who owns the project this submission belongs to.        | Only the professor who created the project can evaluate its submissions. |
| `Sem permissão para cancelar esta matrícula`        | The authenticated student is not the owner of the enrollment.                                       | Students can only cancel their own enrollments.                          |
| `Sem permissão para ver esta submissão`             | The authenticated user is neither the student who submitted nor the professor who owns the project. | Only the submitting student or the project owner can view a submission.  |

---

## 404 Not Found

Returned when the requested resource does not exist.

| Error message              | Cause                                      | Resolution                              |
| -------------------------- | ------------------------------------------ | --------------------------------------- |
| `Projeto não encontrado`   | No project exists with the provided ID.    | Verify the project ID and try again.    |
| `Etapa não encontrada`     | No stage exists with the provided ID.      | Verify the stage ID and try again.      |
| `Matrícula não encontrada` | No enrollment exists with the provided ID. | Verify the enrollment ID and try again. |
| `Submissão não encontrada` | No submission exists with the provided ID. | Verify the submission ID and try again. |
