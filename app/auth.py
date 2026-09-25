from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username, role):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)