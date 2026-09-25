
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse
from app.auth import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Register
@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    username = user.username.strip()

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=username,
        password=hash_password(user.password),
        role="doctor"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    username = form_data.username.strip()

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    token = create_access_token(
        existing_user.username,
        existing_user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
