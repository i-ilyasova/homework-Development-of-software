import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import security as sec_module
from database import Base, get_db
from main import app

TEST_DB_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_state():
    sec_module._blacklist.clear()
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_payload():
    return {
        "username": "admin_user",
        "email": "admin@example.com",
        "password": "Admin1234",
        "role": "admin",
    }


@pytest.fixture
def readonly_payload():
    return {
        "username": "readonly_user",
        "email": "readonly@example.com",
        "password": "Readonly1234",
        "role": "readonly",
    }


@pytest.fixture
def registered_admin(client, admin_payload):
    client.post("/auth/register", json=admin_payload)
    return admin_payload


@pytest.fixture
def registered_readonly(client, readonly_payload):
    client.post("/auth/register", json=readonly_payload)
    return readonly_payload


@pytest.fixture
def admin_token(client, registered_admin):
    response = client.post("/auth/login", json={
        "username": registered_admin["username"],
        "password": registered_admin["password"],
    })
    return response.json()["access_token"]


@pytest.fixture
def readonly_token(client, registered_readonly):
    response = client.post("/auth/login", json={
        "username": registered_readonly["username"],
        "password": registered_readonly["password"],
    })
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def readonly_headers(readonly_token):
    return {"Authorization": f"Bearer {readonly_token}"}
