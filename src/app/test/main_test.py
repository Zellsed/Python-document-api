import pytest
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

@pytest.fixture
def created_document():
    payload = {
        "title": "Fixture Document",
        "content": "Content from fixture",
    }
    response = client.post("/documents", json=payload)
    doc_data = response.json()

    yield doc_data

    doc_id = doc_data["id"]
    client.delete(f"/documents/{doc_id}")


def test_create_document():
    payload = {
        "title": "Test Document",
        "content": "This is a test document",
    }
    response = client.post("/documents", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == "Test Document"
    assert response_data["content"] == "This is a test document"

def test_get_document(created_document):
    document_id = created_document["id"]

    response = client.get(f"/documents/{document_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == "Fixture Document"
    assert response_data["id"] == document_id

def test_update_invalidates_cache(created_document):
    document_id = created_document["id"]

    get_before = client.get(f"/documents/{document_id}")

    assert get_before.status_code == 200
    assert get_before.json()["title"] == "Fixture Document"

    payload = {
        "title": "Updated Document",
        "content": "Updated content",
    }

    put_res = client.put(f"/documents/{document_id}", json=payload)

    assert put_res.status_code == 200

    get_after = client.get(f"/documents/{document_id}")

    assert get_after.status_code == 200
    assert get_after.json()["title"] == "Updated Document"
    assert get_after.json()["content"] == "Updated content"

def test_put_document(created_document):
    document_id = created_document["id"]
    payload = {
        "title": "Updated Document",
        "content": "Updated content",
    }
    response = client.put(f"/documents/{document_id}", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["title"] == "Updated Document"
    assert response_data["id"] == document_id

def test_delete_document(created_document):
    document_id = created_document["id"]
    response = client.delete(f"/documents/{document_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["message"] == "Document deleted successfully"

    response = client.get(f"/documents/{document_id}")
    assert response.status_code == 404

def test_update_document_not_found():
    document_id = 9999
    payload = {
        "title": "Updated Document",
        "content": "Updated content",
    }
    response = client.put(f"/documents/{document_id}", json=payload)
    assert response.status_code == 404

def test_get_document_not_found():
    document_id = 9999
    response = client.get(f"/documents/{document_id}")
    assert response.status_code == 404

def test_delete_document_not_found():
    document_id = 9999
    response = client.delete(f"/documents/{document_id}")
    assert response.status_code == 404