import json
from datetime import timedelta, datetime, timezone
from uuid import uuid4

from jose import jwt, JWTError
from starlette.requests import Request
from starlette.responses import Response


def sign_data(secret_key: str, data: dict, expires_delta: timedelta | None = None, algorithm: str = "HS256"):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_data(secret_key: str, token: str, algorithm: str = "HS256"):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.JWTError:
        return None
    return decoded


def create_session_middleware(secret_key: str, session_cookie_name: str = "evsession", session_ttl=timedelta(days=30)):
    async def session_middleware(request: Request, handler):
        try:
            token = decode_data(secret_key, request.cookies.get(session_cookie_name))
            if not token or "session_id" not in token:
                raise JWTError
        except (JWTError, AttributeError):
            token = {"session_id": str(uuid4())}

        request.state.session_cookie = token

        response: Response = await handler(request)

        update = response.headers.get("update-session-cookie", "{}")
        if update:
            try:
                token.update(json.loads(update))
            except json.JSONDecodeError:
                print("[session_middleware]: Failed to decode update session cookie")

        response.set_cookie(key=session_cookie_name, value=sign_data(secret_key, token), httponly=True,
                            samesite="strict",
                            expires=datetime.now(timezone.utc) + session_ttl)
        return response

    return session_middleware
