"""Pipeline de predicción: modelo + datos nuevos → predicciones."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.modelos.entrenamiento import cargar
from src.utils.logging_config import configurar_logs

configurar_logs()
logger = logging.getLogger("dm.pipeline.prediccion")

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "assets" / "datos" / "nuevos.parquet"
SALIDA = RAIZ / "assets" / "datos" / "predicciones.parquet"


def ejecutar(ruta_entrada: Path = ENTRADA, ruta_salida: Path = SALIDA) -> Path:
    """Aplica el modelo entrenado a un lote de datos nuevos."""
    modelo = cargar()
    df = pd.read_parquet(ruta_entrada)
    X = df.select_dtypes("number").to_numpy()

    logger.info("Prediciendo sobre %d filas", len(X))
    df["prediccion"] = modelo.predict(X)
    if hasattr(modelo, "predict_proba"):
        df["probabilidad"] = modelo.predict_proba(X).max(axis=1)

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_salida, index=False)
    logger.info("Predicciones escritas en %s", ruta_salida)
    return ruta_salida


if __name__ == "__main__":
    ejecutar()
