import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Remove if already present
    client.post(f"/activities/{activity}/remove", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate sign up should fail
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # Remove
    response3 = client.post(f"/activities/{activity}/remove", params={"email": email})
    assert response3.status_code == 200
    assert f"Removed {email}" in response3.json()["message"]
    # Remove again should fail
    response4 = client.post(f"/activities/{activity}/remove", params={"email": email})
    assert response4.status_code == 404
