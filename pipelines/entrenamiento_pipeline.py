"""Pipeline de entrenamiento: dataset limpio → modelo.

No promueve el modelo sin validación manual previa (anexo de ética, punto 4).
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.modelos.entrenamiento import entrenar, guardar
from src.utils.logging_config import configurar_logs

configurar_logs()
logger = logging.getLogger("dm.pipeline.entrenamiento")

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "assets" / "datos" / "limpios.parquet"
COLUMNA_OBJETIVO = "objetivo"


def ejecutar(ruta_datos: Path = DATOS) -> Path:
    """Entrena el modelo y lo persiste en `models/`."""
    logger.info("Leyendo dataset limpio de %s", ruta_datos)
    df = pd.read_parquet(ruta_datos)

    if COLUMNA_OBJETIVO not in df.columns:
        raise ValueError(f"Falta la columna objetivo '{COLUMNA_OBJETIVO}'")

    X = df.drop(columns=[COLUMNA_OBJETIVO]).select_dtypes("number").to_numpy()
    y = df[COLUMNA_OBJETIVO].to_numpy()

    logger.info("Entrenando con %d filas y %d características", *X.shape)
    modelo = entrenar(X, y)

    ruta = guardar(modelo)
    logger.info("Modelo guardado en %s", ruta)
    logger.warning("PENDIENTE: validación manual antes de desplegar")
    return ruta


if __name__ == "__main__":
    ejecutar()
