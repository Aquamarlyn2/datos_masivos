"""Pruebas de ingeniería de características."""

import pandas as pd

from src.caracteristicas.ingenieria import (
    agregar_ratios,
    codificar_categoricas,
    ventana_movil,
)


def test_agregar_ratios_evita_division_por_cero():
    df = pd.DataFrame({"a": [10, 20], "b": [2, 0]})
    resultado = agregar_ratios(df, "a", "b", "ratio")
    assert resultado["ratio"].iloc[0] == 5.0
    assert pd.isna(resultado["ratio"].iloc[1])


def test_codificar_categoricas():
    df = pd.DataFrame({"color": ["rojo", "azul", "rojo"], "valor": [1, 2, 3]})
    resultado = codificar_categoricas(df, ["color"])
    assert "color_rojo" in resultado.columns
    assert resultado["color_rojo"].sum() == 2


def test_ventana_movil_genera_columnas():
    df = pd.DataFrame({"y": range(10)})
    resultado = ventana_movil(df, "y", ventana=3)
    assert "y_media_3" in resultado.columns
    assert pd.isna(resultado["y_media_3"].iloc[0])
