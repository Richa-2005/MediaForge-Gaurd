from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.router import api_router
from app.core.config import settings
from app.database.session import get_db
from app.models.base import Base


def make_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as db:
            yield db

    app = FastAPI()
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


def test_register_returns_token_and_user():
    client = make_client()

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "Analyst@Example.com",
            "password": "strong-password",
            "full_name": "Media Analyst",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["user"]["email"] == "analyst@example.com"
    assert payload["user"]["full_name"] == "Media Analyst"
    assert payload["user"]["is_active"] is True


def test_register_rejects_duplicate_email():
    client = make_client()
    payload = {
        "email": "analyst@example.com",
        "password": "strong-password",
    }

    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409


def test_login_and_me_round_trip():
    client = make_client()
    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "analyst@example.com",
            "password": "strong-password",
        },
    )
    token = register.json()["access_token"]

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "analyst@example.com",
            "password": "strong-password",
        },
    )

    assert login.status_code == 200
    login_token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "analyst@example.com"
    assert token


def test_me_requires_bearer_token():
    client = make_client()

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
