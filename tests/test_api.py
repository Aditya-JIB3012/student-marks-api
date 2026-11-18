import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from main import app

client = TestClient(app)


# ── Test 1: Health endpoint ──────────────────────────────────────────────────
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ── Test 2: Get all students returns a list ──────────────────────────────────
def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert "students" in data
    assert isinstance(data["students"], list)
    assert data["total"] >= 3          # at least the 3 seed records


# ── Test 3: Add a new student ────────────────────────────────────────────────
def test_add_student():
    payload = {"name": "David Lee", "subject": "Physics", "marks": 85}
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "David Lee"
    assert body["marks"] == 85
    assert "id" in body


# ── Test 4: Get student by ID ─────────────────────────────────────────────────
def test_get_student_by_id():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


# ── Test 5: Get non-existent student returns 404 ─────────────────────────────
def test_get_student_not_found():
    response = client.get("/students/9999")
    assert response.status_code == 404
