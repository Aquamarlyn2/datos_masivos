"""Detección de deriva (data drift) entre el set de entrenamiento y producción.

Implementa la revisión de equidad y calidad exigida por los puntos 5 y 10
del anexo de ética.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger("dm.monitoring.deriva")

RAIZ = Path(__file__).resolve().parents[1]
REFERENCIA = RAIZ / "assets" / "datos" / "limpios.parquet"
ACTUAL = RAIZ / "assets" / "datos" / "predicciones.parquet"
UMBRAL = 0.1   # diferencia relativa tolerable en la media


def psi(esperado: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """Índice de estabilidad poblacional (PSI) entre dos distribuciones."""
    cortes = np.quantile(esperado, np.linspace(0, 1, bins + 1))
    cortes[0], cortes[-1] = -np.inf, np.inf
    e = np.histogram(esperado, bins=cortes)[0] / len(esperado)
    a = np.histogram(actual, bins=cortes)[0] / len(actual)
    e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
    return float(np.sum((a - e) * np.log(a / e)))


def ejecutar(referencia: Path = REFERENCIA, actual: Path = ACTUAL) -> dict:
    """Compara la distribución de referencia con la observada en producción."""
    ref = pd.read_parquet(referencia).select_dtypes("number")
    act = pd.read_parquet(actual).select_dtypes("number")

    comunes = [c for c in ref.columns if c in act.columns]
    resultados: dict[str, dict] = {}

    for col in comunes:
        r, a = ref[col].dropna().to_numpy(), act[col].dropna().to_numpy()
        if len(r) < 10 or len(a) < 10:
            continue
        valor_psi = psi(r, a)
        deriva = valor_psi > UMBRAL
        resultados[col] = {"psi": round(valor_psi, 4), "deriva": deriva}
        if deriva:
            logger.warning("Deriva detectada en '%s' (PSI=%.4f)", col, valor_psi)

    if not any(v["deriva"] for v in resultados.values()):
        logger.info("Sin deriva significativa en %d variables", len(resultados))

    return resultados


if __name__ == "__main__":
    import json

    print(json.dumps(ejecutar(), indent=2, ensure_ascii=False))
