"""Definición y entrenamiento de modelos.

El código generado por IA nunca se despliega sin validación manual
(anexo de ética, puntos 1 y 4). Toda promoción a `models/` requiere
pasar `tests/`.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split

RAIZ = Path(__file__).resolve().parents[2]
DIR_MODELOS = RAIZ / "models"


def entrenar(X: np.ndarray, y: np.ndarray, semilla: int = 42) -> RandomForestClassifier:
    """Entrena un clasificador de bosque aleatorio."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=semilla, stratify=y
    )
    modelo = RandomForestClassifier(n_estimators=300, random_state=semilla, n_jobs=-1)
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)
    print(classification_report(y_test, pred))
    print(f"F1 macro: {f1_score(y_test, pred, average='macro'):.4f}")
    return modelo


def guardar(modelo, nombre: str = "modelo_rf") -> Path:
    """Persiste el modelo con sus hiperparámetros."""
    DIR_MODELOS.mkdir(parents=True, exist_ok=True)
    destino = DIR_MODELOS / f"{nombre}.joblib"
    joblib.dump(modelo, destino)
    return destino


def cargar(nombre: str = "modelo_rf"):
    """Carga un modelo entrenado desde `models/`."""
    return joblib.load(DIR_MODELOS / f"{nombre}.joblib")
