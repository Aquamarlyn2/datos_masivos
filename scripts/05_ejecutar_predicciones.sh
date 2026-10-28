#!/usr/bin/env bash
# Consulta la API de inferencia.
# Uso: bash scripts/05_ejecutar_predicciones.sh
set -euo pipefail

API="${API_URL:-http://localhost:8000}"

echo "==> Salud del servicio"
curl -sf "$API/health" | jq .

echo "==> Predicción de ejemplo"
curl -sf -X POST "$API/predecir" \
  -H "Content-Type: application/json" \
  -d '{"caracteristicas": [0.5, -1.2, 0.3, 0.8, -0.4, 1.1, 0.0, 0.6]}' | jq .
