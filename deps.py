from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.models import User
from auth.service import get_user
from auth.utils import verify_token, is_valid_token_type
from database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DatabaseDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: TokenDep, db: DatabaseDep) -> User:
    payload = verify_token(token)
    is_valid_token_type(payload, "access")

    user_id: int = payload.get("sub")

    return get_user(db, user_id)


CurrentUserDep = Annotated[User, Depends(get_current_user)]
