"""Pruebas del módulo de preprocesamiento."""

import pandas as pd
import pytest

from src.preprocesamiento.limpieza import (
    anonimizar,
    eliminar_duplicados,
    rellenar_nulos,
)


@pytest.fixture
def df_crudo() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "nombre": ["ana", "luis", "ana"],
            "correo": ["a@x.com", "l@x.com", "a@x.com"],
            "edad": [30, None, 30],
            "ingreso": [100.0, 200.0, 100.0],
        }
    )


def test_anonimizar_no_deja_datos_originales(df_crudo):
    resultado = anonimizar(df_crudo)
    assert "ana" not in resultado["nombre"].values
    assert resultado["nombre"].iloc[0] == resultado["nombre"].iloc[2]  # mismo hash


def test_anonimizar_es_determinista(df_crudo):
    assert anonimizar(df_crudo)["correo"].tolist() == anonimizar(df_crudo)["correo"].tolist()


def test_eliminar_duplicados(df_crudo):
    assert len(eliminar_duplicados(df_crudo, ["nombre"])) == 2


def test_rellenar_nulos_mediana(df_crudo):
    resultado = rellenar_nulos(df_crudo, "mediana")
    assert resultado["edad"].isna().sum() == 0
    assert resultado["edad"].iloc[1] == 30.0
