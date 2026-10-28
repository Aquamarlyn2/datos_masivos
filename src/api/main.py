"""API de inferencia — servicio de modelos en producción.

Cumple el punto 4 del anexo de ética: el modelo servido aquí pasó por
validación manual y por las pruebas de `tests/`.
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel, Field
from starlette.responses import Response

logger = logging.getLogger("dm.api")

RAIZ = Path(__file__).resolve().parents[2]

PETICIONES = Counter("dm_peticiones_total", "Peticiones atendidas", ["ruta", "estado"])
LATENCIA = Histogram("dm_latencia_segundos", "Latencia de inferencia")

modelo = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo
    ruta = RAIZ / "models" / "modelo_rf.joblib"
    if ruta.exists():
        import joblib

        modelo = joblib.load(ruta)
        logger.info("Modelo cargado desde %s", ruta)
    else:
        logger.warning("No se encontró el modelo en %s; /predecir devolverá 503", ruta)
    yield
    modelo = None


app = FastAPI(
    title="datos_masivos · API de inferencia",
    version="1.0.0",
    lifespan=lifespan,
)


class EntradaPrediccion(BaseModel):
    caracteristicas: list[float] = Field(..., description="Vector de características del modelo")


class SalidaPrediccion(BaseModel):
    prediccion: int
    probabilidad: float | None = None


@app.get("/health")
def salud() -> dict:
    """Sonda de salud consumida por Docker y por el monitoreo."""
    PETICIONES.labels(ruta="/health", estado="200").inc()
    return {"estado": "ok", "modelo_cargado": modelo is not None}


@app.post("/predecir", response_model=SalidaPrediccion)
def predecir(entrada: EntradaPrediccion) -> SalidaPrediccion:
    """Ejecuta inferencia sobre el modelo cargado."""
    if modelo is None:
        PETICIONES.labels(ruta="/predecir", estado="503").inc()
        raise HTTPException(status_code=503, detail="Modelo no disponible")

    inicio = time.perf_counter()
    try:
        import numpy as np

        X = np.asarray(entrada.caracteristicas, dtype=float).reshape(1, -1)
        pred = int(modelo.predict(X)[0])
        proba = None
        if hasattr(modelo, "predict_proba"):
            proba = float(modelo.predict_proba(X).max())
    except Exception as exc:  # noqa: BLE001
        PETICIONES.labels(ruta="/predecir", estado="400").inc()
        raise HTTPException(status_code=400, detail=f"Entrada inválida: {exc}") from exc
    finally:
        LATENCIA.observe(time.perf_counter() - inicio)

    PETICIONES.labels(ruta="/predecir", estado="200").inc()
    return SalidaPrediccion(prediccion=pred, probabilidad=proba)


@app.get("/metrics")
def metricas() -> Response:
    """Métricas en formato Prometheus (ver `monitoring/`)."""
    return Response(generate_latest(), media_type="text/plain")
