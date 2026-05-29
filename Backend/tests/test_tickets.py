import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test_tickets.db"
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


def _register_and_token(username, email, password="pass123"):
    client.post("/auth/register", json={"username": username, "email": email, "password": password})
    res = client.post("/auth/login", data={"username": username, "password": password})
    return res.json()["access_token"]


def test_create_and_list_tickets():
    token = _register_and_token("user1", "user1@test.com")
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/tickets/", json={"title": "Laptop broken", "description": "Screen cracked"}, headers=headers)
    assert res.status_code == 201
    assert res.json()["title"] == "Laptop broken"

    tickets = client.get("/tickets/", headers=headers)
    assert tickets.status_code == 200
    assert len(tickets.json()) == 1


def test_ticket_detail():
    token = _register_and_token("user2", "user2@test.com")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/tickets/", json={"title": "VPN issue", "description": "Cannot connect"}, headers=headers)
    ticket_id = res.json()["id"]

    detail = client.get(f"/tickets/{ticket_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == ticket_id


def test_add_comment():
    token = _register_and_token("user3", "user3@test.com")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/tickets/", json={"title": "Printer offline", "description": "Not printing"}, headers=headers)
    ticket_id = res.json()["id"]

    comment = client.post(f"/tickets/{ticket_id}/comments", json={"content": "Rebooted the printer"}, headers=headers)
    assert comment.status_code == 201
    assert comment.json()["content"] == "Rebooted the printer"
