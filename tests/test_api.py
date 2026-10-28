"""Pruebas de integración de la API de inferencia."""

from fastapi.testclient import TestClient

from src.api.main import app


def test_health_responde_ok():
    with TestClient(app) as cliente:
        r = cliente.get("/health")
    assert r.status_code == 200
    assert r.json()["estado"] == "ok"


def test_prediccion_sin_modelo_devuelve_503():
    with TestClient(app) as cliente:
        r = cliente.post("/predecir", json={"caracteristicas": [0.1] * 8})
    assert r.status_code in (400, 503)


def test_metricas_expuestas():
    with TestClient(app) as cliente:
        r = cliente.get("/metrics")
    assert r.status_code == 200
    assert "dm_peticiones_total" in r.text
