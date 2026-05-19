from fastapi.testclient import TestClient
from app.main import app  # Adjusted import based on your app location

def test_create_request():
    client = TestClient(app)
    response = client.post("/api/v1/requests", json={
        "query": "What is the chemical formula for water?",
        "language": "en"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "pending"