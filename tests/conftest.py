import pytest
from fastapi.testclient import TestClient
from app.services import file_service

@pytest.fixture
def client(tmp_path):
    # Use a temporary empty db.json for tests
    file_service.FILE_PATH = tmp_path / "db.json"
    from app.main import app  # Import AFTER redirecting FILE_PATH
    return TestClient(app)