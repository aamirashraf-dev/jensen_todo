import pytest
from fastapi.testclient import TestClient

from app.services import file_service

def test_list_empty(client: TestClient):
    # Guarantee the test DB is blank
    file_service.write_db([])

    res = client.get("/todos")
    assert res.status_code == 200
    assert res.json() == []



def test_create_todo(client: TestClient):
    payload = {"id": 0, "title": "Test Todo", "description": "Testing creation", "completed": False}
    res = client.post("/todos", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    assert isinstance(data["id"], int)


def test_get_todo_by_id(client: TestClient):
    # Arrange: create one
    payload = {"id": 0, "title": "Fetch Me", "description": "", "completed": False}
    created = client.post("/todos", json=payload)
    assert created.status_code == 201
    todo_id = created.json()["id"]

    # Act
    res = client.get(f"/todos/{todo_id}")

    # Assert
    assert res.status_code == 200
    assert res.json()["id"] == todo_id
    assert res.json()["title"] == "Fetch Me"


def test_update_todo(client: TestClient):
    # Arrange: create one
    payload = {"id": 0, "title": "Old", "description": "", "completed": False}
    created = client.post("/todos", json=payload)
    assert created.status_code == 201
    todo_id = created.json()["id"]

    # Act: update it
    updated_payload = {
        "id": todo_id,
        "title": "New",
        "description": "Updated",
        "completed": True
    }
    res = client.put(f"/todos/{todo_id}", json=updated_payload)

    # Assert
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == todo_id
    assert data["title"] == "New"
    assert data["description"] == "Updated"
    assert data["completed"] is True


def test_delete_todo(client: TestClient):
    # Arrange: create one to delete
    payload = {"id": 0, "title": "To remove", "description": "", "completed": False}
    created = client.post("/todos", json=payload)
    assert created.status_code == 201
    todo_id = created.json()["id"]

    # Act: delete it
    res = client.delete(f"/todos/{todo_id}")

    # Assert
    assert res.status_code == 200
    # Match your API message EXACTLY; if your router returns a different text, adjust below:
    assert res.json()["message"] in (f"Todo {todo_id} deleted", f"Todo {todo_id} deleted successfully")

    # And confirm it’s gone
    res2 = client.get(f"/todos/{todo_id}")
    assert res2.status_code == 404