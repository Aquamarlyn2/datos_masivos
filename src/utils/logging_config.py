"""Configuración central de logs.

Los logs se escriben en `config/` y se rotan (ver `config/logging.yml`).
"""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
CONFIG = RAIZ / "config" / "logging.yml"


def configurar_logs() -> None:
    """Carga la configuración de logging desde `config/logging.yml`."""
    if CONFIG.exists():
        with open(CONFIG, encoding="utf-8") as f:
            logging.config.dictConfig(yaml.safe_load(f))
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        )
