**Response — status 400:**

```html
<!doctype html>
<html lang="en">
  <title>400 Bad Request</title>
  <h1>Bad Request</h1>
  <p>Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)</p>
</html>
```

---

## Expected Behavior

**Response — status 400:**

```json
{
  "erro": "Nenhum dado enviado"
}
```

---

## Steps to Reproduce

1. Start the API and database using `docker compose up`.
2. Send a POST request to `http://localhost:5001/register` with the header `Content-Type: application/json` and an empty body.
3. Observe the response format and content.

---

## Root Cause

Flask's `request.get_json()` method raises an internal exception when it receives an empty body with a `Content-Type: application/json` header. Without error handling in place, the Werkzeug framework (Flask's underlying HTTP layer) intercepted the exception and returned its default HTML error page, bypassing the application's JSON response logic entirely.

This meant that any client sending a malformed request to this endpoint would receive an HTML response instead of JSON, and would also see a raw Python error message exposing internal framework details.

---

## Fix Applied

The `get_json()` call was updated to use the `silent=True` parameter across all route files. This instructs Flask to return `None` instead of raising an exception when the body is missing or malformed, allowing the application to handle the case explicitly and return a consistent JSON error response.

**Before:**

```python
dados = request.get_json()
```

**After:**

```python
dados = request.get_json(silent=True)

if not dados:
    return jsonify({'erro': 'Nenhum dado enviado'}), 400
```

This change was applied to all route files: `auth.py`, `projetos.py`, `etapas.py`, `matriculas.py`, and `submissoes.py`.

---

## Verification

After the fix was applied, the endpoint was retested by sending a POST request to `/register` with an empty body and the `Content-Type: application/json` header. The API returned the expected JSON response with status 400 and the error message `"Nenhum dado enviado"`. The HTML response no longer appears under any tested condition.

---

## Prevention

Two practices would prevent this class of issue from reaching production:

1. **Input validation at the entry point.** Every route that expects a request body should validate the parsed result before processing it. The `silent=True` pattern combined with an explicit null check is a reliable guard against empty or malformed bodies.

2. **Automated test coverage for edge cases.** A test case covering requests with empty bodies (CT-006) was added to the test suite. This test is now part of the automated regression suite and will catch any regression of this behavior in future changes.
