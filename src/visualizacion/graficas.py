"""Visualización de resultados."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DIR_ASSETS = RAIZ / "assets"


def grafica_importancia(importancias, columnas, nombre: str = "importancia") -> Path:
    """Genera una gráfica de barras de importancia de características."""
    serie = pd.Series(importancias, index=columnas).sort_values()
    ax = serie.plot.barh(figsize=(8, max(4, len(serie) * 0.25)))
    ax.set_title("Importancia de características")
    ax.set_xlabel("Importancia relativa")
    DIR_ASSETS.mkdir(parents=True, exist_ok=True)
    destino = DIR_ASSETS / f"{nombre}.png"
    ax.figure.tight_layout()
    ax.figure.savefig(destino, dpi=150)
    plt.close(ax.figure)
    return destino
