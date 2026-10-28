#!/usr/bin/env bash
# Despliega la pila de contenedores.
# Uso: bash scripts/02_levantar_servicios.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

if [[ ! -f deployment/.env ]]; then
  echo "==> Creando deployment/.env desde la plantilla"
  cp deployment/.env.example deployment/.env
  echo "REVISA deployment/.env y cambia las contraseñas antes de continuar." >&2
  exit 1
fi

echo "==> Escaneo de seguridad de las imágenes base (Trivy)"
if command -v trivy >/dev/null; then
  trivy image --severity HIGH,CRITICAL --exit-code 1 \
    quay.io/jupyter/scipy-notebook:latest || \
    echo "ADVERTENCIA: Trivy reportó hallazgos; revisar antes de exponer el servicio."
fi

echo "==> Construyendo imágenes locales (ARM64)"
docker compose -f deployment/docker-compose.yml build

echo "==> Levantando servicios"
docker compose -f deployment/docker-compose.yml up -d

echo "==> Esperando a que la base de datos esté sana"
for i in $(seq 1 30); do
  if docker compose -f deployment/docker-compose.yml ps db | grep -q healthy; then
    break
  fi
  sleep 2
done

echo "==> Estado final"
docker compose -f deployment/docker-compose.yml ps
echo "LISTO."
