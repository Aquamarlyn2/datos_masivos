"""Ingeniería de características."""

from __future__ import annotations

import pandas as pd


def agregar_ratios(df: pd.DataFrame, numerador: str, denominador: str, nombre: str) -> pd.DataFrame:
    """Añade una columna de razón evitando la división por cero."""
    df = df.copy()
    df[nombre] = df[numerador] / df[denominador].replace(0, pd.NA)
    return df


def codificar_categoricas(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """Aplica one-hot encoding a las columnas indicadas."""
    return pd.get_dummies(df, columns=columnas, dtype=int)


def ventana_movil(df: pd.DataFrame, columna: str, ventana: int = 7) -> pd.DataFrame:
    """Añade media y desviación móvil de una columna temporal."""
    df = df.copy()
    df[f"{columna}_media_{ventana}"] = df[columna].rolling(ventana).mean()
    df[f"{columna}_std_{ventana}"] = df[columna].rolling(ventana).std()
    return df
