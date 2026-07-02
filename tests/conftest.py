import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure python knows where the backend folder is
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

@pytest.fixture
def client():
    from backend.app.main import app
    return TestClient(app)
