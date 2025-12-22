Security & Testing Notes
=========================

Required environment variables
- `ADMIN_API_KEY` — optional. If set, requests with header `X-API-KEY` equal to this value are treated as admin.
- `JWT_SECRET_KEY` — required for JWT-based admin tokens. Tokens must carry a `roles` claim including `admin`.
- `ALLOWED_ORIGINS` — comma-separated allowed CORS origins for production.

Generating a test JWT (Python + PyJWT)
```python
import jwt, os
os.environ['JWT_SECRET_KEY'] = 'your-secret'
token = jwt.encode({'roles': ['admin']}, os.environ['JWT_SECRET_KEY'], algorithm='HS256')
print(token)
```

Running tests
1. Install test deps (in `Backend`):
```bash
pip install -r requirements.txt
pip install pytest
```
2. Run pytest:
```bash
pytest -q Backend/tests
```

Notes
- Tests are unit-style and run in-process against the FastAPI `app`.
- Do NOT store real secret keys in test or CI logs. Use environment variables or secret managers.

CI Secrets & GitHub Actions
---------------------------

The CI workflow expects the repository to have the following GitHub Actions secrets set (Repository → Settings → Secrets → Actions):

- `ADMIN_API_KEY` (optional): if set, admin API key used by integration tests and for admin access in the app.
- `JWT_SECRET_KEY` (recommended): secret used to verify JWTs when testing auth-protected endpoints.
- `ALLOWED_ORIGINS` (optional): comma-separated origins allowed by CORS in production builds.
- `ALLOWED_ORIGINS` (optional): comma-separated origins allowed by CORS in production builds.
- `SLACK_WEBHOOK` (optional): Incoming Slack webhook URL. When set, the CI notification workflow will post a message to this webhook on failed CI runs.

To add a secret:

1. Visit your repository on GitHub.
2. Go to `Settings` → `Secrets and variables` → `Actions` → `New repository secret`.
3. Add the secret name and value, then click `Add secret`.

CI will run the backend test suite and the frontend build on every push and pull request to `main`/`master`. Secrets are not printed to logs; ensure any additional secrets needed by your environment are added securely.

