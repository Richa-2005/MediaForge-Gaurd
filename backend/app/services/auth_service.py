import base64
import binascii
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import UserCreate


PASSWORD_ITERATIONS = 310_000
PASSWORD_SCHEME = "pbkdf2_sha256"


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    ).hex()
    return f"{PASSWORD_SCHEME}${PASSWORD_ITERATIONS}${salt}${digest}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        scheme, iterations, salt, digest = hashed_password.split("$", 3)
        if scheme != PASSWORD_SCHEME:
            return False
        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations),
        ).hex()
    except (TypeError, ValueError):
        return False

    return hmac.compare_digest(candidate, digest)


def get_user_by_email(email: str, db: Session) -> User | None:
    return db.scalar(
        select(User).where(User.email == normalize_email(email))
    )


def create_user(payload: UserCreate, db: Session) -> User:
    email = normalize_email(payload.email)

    if get_user_by_email(email, db) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        email=email,
        full_name=payload.full_name.strip() if payload.full_name else None,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user = get_user_by_email(email, db)

    if user is None or not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled.",
        )

    return user


def create_access_token(user: User) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": int(expires_at.timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
    }
    return _encode_jwt(payload)


def decode_access_token(token: str) -> dict[str, Any]:
    payload = _decode_jwt(token)
    expires_at = payload.get("exp")

    if not isinstance(expires_at, int) or expires_at < int(
        datetime.now(timezone.utc).timestamp()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def _encode_jwt(payload: dict[str, Any]) -> str:
    header = {
        "alg": settings.JWT_ALGORITHM,
        "typ": "JWT",
    }
    signing_input = ".".join(
        [
            _base64url_json(header),
            _base64url_json(payload),
        ]
    )
    signature = _sign(signing_input)
    return f"{signing_input}.{signature}"


def _decode_jwt(token: str) -> dict[str, Any]:
    try:
        header_segment, payload_segment, signature = token.split(".", 2)
    except ValueError as exc:
        raise _invalid_token_error() from exc

    signing_input = f"{header_segment}.{payload_segment}"
    expected_signature = _sign(signing_input)

    if not hmac.compare_digest(signature, expected_signature):
        raise _invalid_token_error()

    try:
        header = _base64url_decode_json(header_segment)
        payload = _base64url_decode_json(payload_segment)
    except (ValueError, json.JSONDecodeError, binascii.Error) as exc:
        raise _invalid_token_error() from exc

    if header.get("alg") != settings.JWT_ALGORITHM:
        raise _invalid_token_error()

    return payload


def _sign(value: str) -> str:
    secret = settings.JWT_SECRET_KEY.get_secret_value().encode("utf-8")
    digest = hmac.new(secret, value.encode("utf-8"), hashlib.sha256).digest()
    return _base64url_encode(digest)


def _base64url_json(value: dict[str, Any]) -> str:
    serialized = json.dumps(value, separators=(",", ":")).encode("utf-8")
    return _base64url_encode(serialized)


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _base64url_decode_json(value: str) -> dict[str, Any]:
    padding = "=" * (-len(value) % 4)
    decoded = base64.urlsafe_b64decode(f"{value}{padding}")
    payload = json.loads(decoded)

    if not isinstance(payload, dict):
        raise ValueError("JWT segment must decode to an object.")

    return payload


def _invalid_token_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
