import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

auth_scheme = HTTPBearer(auto_error=False)


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)) -> dict:
    """Verify a JWT from the Authorization: Bearer header.

    Uses `JWT_SECRET_KEY` (environment) and HS256. Returns token payload dict
    on success, raises HTTPException on failure.
    """
    secret = os.environ.get("JWT_SECRET_KEY")
    if not secret:
        raise HTTPException(status_code=503, detail="JWT not configured on server")

    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing credentials")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
