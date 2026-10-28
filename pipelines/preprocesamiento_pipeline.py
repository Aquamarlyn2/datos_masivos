"""Pipeline de preprocesamiento: datos crudos → dataset limpio.

Reglas del proyecto:
  - Anonimizar antes de cualquier automatización (anexo de ética, punto 2).
  - Idempotente: repetirlo sobre la misma entrada da el mismo resultado.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.preprocesamiento.limpieza import (
    anonimizar,
    eliminar_duplicados,
    rellenar_nulos,
)
from src.utils.logging_config import configurar_logs

configurar_logs()
logger = logging.getLogger("dm.pipeline.preprocesamiento")

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "assets" / "datos" / "crudos.csv"
SALIDA = RAIZ / "assets" / "datos" / "limpios.parquet"


def ejecutar(ruta_entrada: Path = ENTRADA, ruta_salida: Path = SALIDA) -> Path:
    """Ejecuta el pipeline completo y devuelve la ruta del dataset limpio."""
    logger.info("Leyendo datos crudos de %s", ruta_entrada)
    df = pd.read_csv(ruta_entrada)

    logger.info("Anonimizando columnas identificables")
    df = anonimizar(df)

    logger.info("Eliminando duplicados")
    df = eliminar_duplicados(df)

    logger.info("Rellenando nulos")
    df = rellenar_nulos(df, estrategia="mediana")

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_salida, index=False)
    logger.info("Dataset limpio escrito en %s (%d filas)", ruta_salida, len(df))
    return ruta_salida


if __name__ == "__main__":
    ejecutar()
