from pathlib import Path


def test_health_includes_catalyst_release(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    release = response.json()["release"]
    assert release["version"] == "0.4.0"
    assert release["label"] == "0.4: Expansion"
    assert release["codename"] == "Expansion"


def test_frontend_displays_catalyst_version():
    index = Path("frontend/index.html").read_text()
    assert "0.4: Expansion" in index
    assert "aria-current=\"page\"" in index
    assert "role=\"tablist\"" in index
    assert "aria-selected=\"true\"" in index
