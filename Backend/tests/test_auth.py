import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_register_and_login():
    res = client.post("/auth/register", json={"username": "alice", "email": "alice@test.com", "password": "secret123"})
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "alice"
    assert data["role"] == "user"

    login = client.post("/auth/login", data={"username": "alice", "password": "secret123"})
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_duplicate_username():
    client.post("/auth/register", json={"username": "bob", "email": "bob@test.com", "password": "pass"})
    res = client.post("/auth/register", json={"username": "bob", "email": "bob2@test.com", "password": "pass"})
    assert res.status_code == 400


def test_wrong_password():
    client.post("/auth/register", json={"username": "carol", "email": "carol@test.com", "password": "mypass"})
    res = client.post("/auth/login", data={"username": "carol", "password": "wrong"})
    assert res.status_code == 401


def test_me_endpoint():
    client.post("/auth/register", json={"username": "dave", "email": "dave@test.com", "password": "pass123"})
    login = client.post("/auth/login", data={"username": "dave", "password": "pass123"})
    token = login.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "dave"
