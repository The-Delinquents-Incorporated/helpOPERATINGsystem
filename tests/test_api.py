import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

def test_health_check_ollama_unreachable(client: TestClient):
    with patch("backend.app.services.ollama.ollama_service.check_health", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = False
        
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["ollama"]["connected"] is False

def test_health_check_ollama_reachable(client: TestClient):
    with patch("backend.app.services.ollama.ollama_service.check_health", new_callable=AsyncMock) as mock_health, \
         patch("backend.app.services.ollama.ollama_service.list_local_models", new_callable=AsyncMock) as mock_models:
        
        mock_health.return_value = True
        mock_models.return_value = [{"name": "llama3:latest"}, {"name": "mistral:latest"}]
        
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["ollama"]["connected"] is True
        assert "llama3:latest" in data["ollama"]["available_models"]

def test_get_elements(client: TestClient):
    response = client.get("/api/elements")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 118
    assert data[0]["symbol"] == "H"
    assert data[1]["symbol"] == "He"

def test_get_element_by_query_success(client: TestClient):
    # Test by Symbol
    response = client.get("/api/elements/H")
    assert response.status_code == 200
    assert response.json()["name"] == "hydrogen"

    # Test by Number
    response = client.get("/api/elements/2")
    assert response.status_code == 200
    assert response.json()["symbol"] == "He"

    # Test by Name
    response = client.get("/api/elements/lithium")
    assert response.status_code == 200
    assert response.json()["atomic_number"] == 3

def test_get_element_by_query_not_found(client: TestClient):
    response = client.get("/api/elements/invalid_element")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_chat_completion_success(client: TestClient):
    mock_response = {
        "model": "llama3",
        "message": {"role": "assistant", "content": "Hello! I am HelpOS."},
        "done": True
    }
    
    with patch("backend.app.services.ollama.ollama_service.generate_chat_completion", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_response
        
        payload = {
            "messages": [{"role": "user", "content": "Hi"}],
            "model": "llama3",
            "stream": False
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        assert response.json()["mode"] == "reasoning"
        assert response.json()["content"] == "Hello! I am HelpOS."

def test_chat_completion_unreachable_ollama(client: TestClient):
    with patch("backend.app.services.ollama.ollama_service.generate_chat_completion", new_callable=AsyncMock) as mock_chat:
        mock_chat.side_effect = RuntimeError("Ollama instance is unreachable")
        
        payload = {
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": False
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 503
        assert "unreachable" in response.json()["detail"]
