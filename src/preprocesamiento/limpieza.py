"""Limpieza y transformación de datos crudos.

Regla del proyecto (anexo de ética, punto 2): ningún dato personal avanza
sin anonimización previa. La función `anonimizar` se ejecuta antes de
cualquier otro paso del pipeline.
"""

from __future__ import annotations

import hashlib

import pandas as pd

COLUMNAS_IDENTIFICABLES = ("nombre", "correo", "telefono", "curp", "rfc", "direccion")


def anonimizar(df: pd.DataFrame, columnas: tuple[str, ...] = COLUMNAS_IDENTIFICABLES) -> pd.DataFrame:
    """Sustituye columnas identificables por su hash SHA-256 truncado."""
    df = df.copy()
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].astype(str).map(
                lambda v: hashlib.sha256(v.encode("utf-8")).hexdigest()[:16]
            )
    return df


def eliminar_duplicados(df: pd.DataFrame, subconjunto: list[str] | None = None) -> pd.DataFrame:
    """Elimina filas duplicadas conservando la primera aparición."""
    return df.drop_duplicates(subset=subconjunto, keep="first").reset_index(drop=True)


def rellenar_nulos(df: pd.DataFrame, estrategia: str = "mediana") -> pd.DataFrame:
    """Rellena valores nulos en columnas numéricas.

    Args:
        estrategia: "mediana" o "media".
    """
    df = df.copy()
    numericas = df.select_dtypes(include="number").columns
    for col in numericas:
        valor = df[col].median() if estrategia == "mediana" else df[col].mean()
        df[col] = df[col].fillna(valor)
    return df
