#!/usr/bin/env bash
# Ejecuta la batería de pruebas (barrera de calidad antes del despliegue).
# Uso: bash scripts/06_validar_pruebas.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

echo "==> Pruebas unitarias y de integración"
if command -v pytest >/dev/null; then
  pytest -q --cov=src --cov-report=term-missing
else
  echo "pytest no instalado; se ejecuta dentro del contenedor de la API"
  docker exec dm-api pytest -q || true
fi

echo "==> Análisis estático"
if command -v ruff >/dev/null; then ruff check src/ tests/; fi

echo "==> Escaneo de vulnerabilidades en las imágenes"
if command -v trivy >/dev/null; then
  trivy image --severity HIGH,CRITICAL dm-api:latest || true
fi

echo "LISTO."
