from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import os
from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

auth_scheme_bearer = HTTPBearer(auto_error=False)

API_KEY_HEADER = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)) -> bool:
    """Simple API key dependency. Compares header to ADMIN_API_KEY env var.

    - Does NOT log or return secret values.
    - Raises 401 when missing or incorrect.
    """
    admin_key = os.environ.get("ADMIN_API_KEY")
    if not admin_key:
        raise HTTPException(status_code=503, detail="Server misconfigured: admin key not set")

    if not api_key or api_key != admin_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return True


def require_admin(api_key: Optional[str] = Security(api_key_header), credentials: Optional[HTTPAuthorizationCredentials] = Security(auth_scheme_bearer)) -> bool:
    """Dependency that accepts either a valid ADMIN_API_KEY header or a valid JWT with admin privileges.

    - If `ADMIN_API_KEY` env var is set and matches header, allow.
    - Otherwise validate JWT from Authorization Bearer token contains `roles` including `admin`.
    This function avoids invoking JWT validation unless needed to prevent misconfiguration errors.
    """
    admin_key = os.environ.get("ADMIN_API_KEY")
    # If API key is configured and matches, allow
    if admin_key and api_key and api_key == admin_key:
        return True

    # Try JWT path only if a bearer token and secret configured
    jwt_secret = os.environ.get("JWT_SECRET_KEY")
    if credentials and jwt_secret:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"]) if token else None
            roles = payload.get("roles") or payload.get("role") or []
            if isinstance(roles, str):
                roles = [roles]
            if payload and "admin" in roles:
                return True
        except Exception:
            pass

    raise HTTPException(status_code=401, detail="Unauthorized")
