import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app  # Assuming your FastAPI app is in backend/main.py
from config.database import get_session

# Override the get_db dependency to use the test database session
def override_get_session(session: Session):
    def _override_get_session():
        try:
            yield session
        finally:
            session.close()
    return _override_get_session

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
def setup_db(session: Session):
    app.dependency_overrides[get_session] = override_get_session(session)
    yield
    session.rollback()
    session.close()

def test_create_topic(client):
    response = client.post("/api/v1/topics", json={"name": "New Topic"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Topic"
    assert "id" in data

def test_get_topics(client):
    response = client.get("/api/v1/topics")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_get_topic(client):
    # First, create a topic
    response = client.post("/api/v1/topics", json={"name": "Test Topic"})
    topic_id = response.json()["id"]

    # Now, get the topic by ID
    response = client.get(f"/api/v1/topics/{topic_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == topic_id
    assert data["name"] == "Test Topic"

def test_post_message(client):
    # First, create a topic
    response = client.post("/api/v1/topics", json={"name": "Test Topic"})
    topic_id = response.json()["id"]

    # Now, post a message to the topic
    response = client.post(f"/api/v1/topics/{topic_id}/messages", json={"author_nickname": "user", "content": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["author_nickname"] == "user"
    assert data["content"] == "Hello"

def test_get_messages_by_topic(client):
    # First, create a topic
    response = client.post("/api/v1/topics", json={"name": "Test Topic"})
    topic_id = response.json()["id"]

    # Post a message to the topic
    client.post(f"/api/v1/topics/{topic_id}/messages", json={"author_nickname": "user", "content": "Hello"})

    # Now, get messages by topic ID
    response = client.get(f"/api/v1/topics/{topic_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) > 0
    assert data["items"][0]["author_nickname"] == "user"
    assert data["items"][0]["content"] == "Hello"
