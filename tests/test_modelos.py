"""Pruebas del entrenamiento de modelos."""

import numpy as np
from sklearn.datasets import make_classification

from src.modelos.entrenamiento import entrenar


def test_entrenar_devuelve_modelo_usable():
    X, y = make_classification(n_samples=200, n_features=8, random_state=42)
    modelo = entrenar(X, y)
    pred = modelo.predict(X[:5])
    assert len(pred) == 5
    assert set(np.unique(pred)).issubset({0, 1})
