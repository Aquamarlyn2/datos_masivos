#!/usr/bin/env bash
# Resumen del estado del Pi y de los servicios.
# Uso: bash monitoring/panel_salud.sh
set -uo pipefail

echo "=============== PANEL DE SALUD ==============="
echo "Fecha:      $(date '+%Y-%m-%d %H:%M:%S')"
echo "Arquitectura: $(uname -m)"
echo

echo "--- Temperatura y throttling ---"
vcgencmd measure_temp
vcgencmd get_throttled

echo
echo "--- Memoria ---"
free -h

echo
echo "--- Disco ---"
df -h / | tail -1

echo
echo "--- Contenedores ---"
docker compose -f "$(dirname "${BASH_SOURCE[0]}")/../deployment/docker-compose.yml" ps

echo
echo "--- Sondas de salud ---"
curl -sf http://localhost:8000/health && echo || echo "API: sin respuesta"
curl -sf -o /dev/null http://localhost:11434/api/tags && echo "Ollama: OK" || echo "Ollama: sin respuesta"

echo
echo "--- Errores recientes ---"
docker compose -f "$(dirname "${BASH_SOURCE[0]}")/../deployment/docker-compose.yml" logs --tail=20 2>/dev/null | grep -i error || echo "Sin errores recientes"
