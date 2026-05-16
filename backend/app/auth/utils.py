import base64
import hashlib
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.settings import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt_rounds=settings.BCRYPT_ROUNDS
)


def prepare_password(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.b64encode(digest)[:72]


def hash_password(password: str) -> str:
    return pwd_context.hash(prepare_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(prepare_password(plain_password), hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )