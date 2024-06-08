from datetime import timedelta, datetime, timezone

from jose import jwt

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
    if not token:
        return None
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.JWTError:
        return None
    return decoded


