from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.models import InquiryResponse

client = TestClient(app)

MOCK_RESPONSE = InquiryResponse(
    category="pakke_sporing",
    summary="Pakken er ikke kommet frem. Sporingsnummer: NO12345678901234567",
    suggested_action="Sjekk sporingsstatus og kontakt transportør",
    confidence=0.95,
    processing_time_ms=123.45,
)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_process_inquiry_success() -> None:
    with patch("app.main.process_inquiry", return_value=MOCK_RESPONSE):
        response = client.post(
            "/inquiries",
            json={
                "text": "Pakken min med nummer NO12345678901234567 er ikke kommet frem",
                "language": "no",
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "pakke_sporing"
    assert "summary" in data
    assert "suggested_action" in data
    assert "confidence" in data
    assert "processing_time_ms" in data


def test_process_inquiry_empty_text() -> None:
    response = client.post("/inquiries", json={"text": "", "language": "no"})
    assert response.status_code == 422
