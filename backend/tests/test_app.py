import os
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# ----------- TEST: GET / (health check) -----------
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Traffic Flow Optimizer API is running"}

# ----------- TEST: POST /emergency (valid + invalid) -----------
def test_trigger_emergency_valid():
    response = client.post("/emergency", params={"direction": "north"})
    assert response.status_code == 200
    assert "Emergency triggered for north" in response.json().get("message")

def test_trigger_emergency_invalid():
    response = client.post("/emergency", params={"direction": "up"})
    assert response.status_code == 400
    assert "error" in response.json()

# ----------- TEST: POST /emergency/clear -----------
def test_clear_emergency():
    response = client.post("/emergency/clear")
    assert response.status_code == 200
    assert response.json() == {"message": "Emergency cleared"}

# ----------- TEST: GET /status -----------
def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert "emergency_mode" in response.json()
    assert "emergency_direction" in response.json()

# ----------- TEST: GET /processed_video/{filename} -----------
def test_get_processed_video_not_found():
    response = client.get("/processed_video/nonexistent.mp4")
    assert response.status_code == 404
    assert response.json() == {"detail": "Processed video not found"}
