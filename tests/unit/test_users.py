import pytest
from app.modules.users.models.user import User, UserRole

def test_create_user(client):
    response = client.post("/api/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "role": "student"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "student"

def test_get_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
