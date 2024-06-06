from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
import uuid
from datetime import datetime, timedelta
from settings import settings

pwd_context = CryptContext(schemes=["django_pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRE = timedelta(days=7)


def create_token(subject: int, token_type: str, expires_delta: timedelta) -> str:
    to_encode = {
        "token_type": token_type,
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "sub": str(subject)
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(subject: int) -> str:
    return create_token(subject, "access", ACCESS_TOKEN_EXPIRE)


def create_refresh_token(subject: int) -> str:
    return create_token(subject, "refresh", REFRESH_TOKEN_EXPIRE)


def is_valid_token_type(payload, expected_token_type: str):
    if 'token_type' in payload and payload['token_type'] == expected_token_type:
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type"
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def refresh_access_token(refresh_token: str) -> str:
    payload = verify_token(refresh_token)
    is_valid_token_type(payload, "refresh")

    new_access_token = create_access_token(payload["sub"])
    return new_access_token
