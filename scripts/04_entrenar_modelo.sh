#!/usr/bin/env bash
# Entrena y guarda el modelo (validación manual obligatoria antes de desplegar).
# Uso: bash scripts/04_entrenar_modelo.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

echo "==> Validando pruebas antes de entrenar"
bash scripts/06_validar_pruebas.sh

echo "==> Entrenando el modelo"
python -m src.modelos.entrenamiento

echo "==> Modelo guardado en models/"
ls -lh models/
echo "LISTO."
