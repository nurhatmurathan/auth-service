from fastapi import APIRouter, HTTPException, status

from deps import DatabaseDep, CurrentUserDep
from . import schemas, services, utils

router = APIRouter()


@router.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: DatabaseDep):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return services.create_user(db, user)


@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_202_ACCEPTED)
def login(user: schemas.UserLogin, db: DatabaseDep):
    db_user = services.get_user_by_email(db, email=user.email)
    if not db_user or not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = utils.create_access_token(subject=db_user.id)
    refresh_token = utils.create_refresh_token(subject=db_user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }


@router.post("/login/verify")
def verify_token_route(token_request: schemas.VerifyToken):
    detail = utils.verify_token(token_request.token)
    return {"detail": detail}


@router.post("/login/refresh", response_model=schemas.AccessToken)
def refresh_token_route(refresh_request: schemas.RefreshToken):
    new_access_token = utils.refresh_access_token(refresh_request.refresh_token)
    return {"access_token": new_access_token}


@router.get("/profile", response_model=schemas.User)
def check_authorization(current_user: CurrentUserDep):
    return current_user
