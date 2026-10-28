#!/usr/bin/env bash
# Instala el runtime de contenedores y Trivy.
# Uso: bash scripts/01_instalar_contenedores.sh
set -euo pipefail

MOTOR="${1:-docker}"   # docker | podman

if [[ "$MOTOR" == "docker" ]]; then
  echo "==> Instalando Docker Engine (ARM64)"
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER"
  sudo systemctl enable --now docker
  docker --version
  docker compose version
elif [[ "$MOTOR" == "podman" ]]; then
  echo "==> Instalando Podman (rootless por defecto)"
  sudo apt-get update -qq
  sudo apt-get install -y -qq podman podman-compose
  podman --version
  podman-compose --version
else
  echo "Motor desconocido: $MOTOR (usar docker o podman)" >&2
  exit 1
fi

echo "==> Verificando soporte de cgroups de memoria"
if ! grep -q memory /sys/fs/cgroup/cgroup.controllers; then
  echo "ADVERTENCIA: falta el cgroup de memoria. Revisa cmdline.txt y reinicia." >&2
fi

echo "==> Arquitectura detectada: $(uname -m)  (debe ser aarch64)"
echo "LISTO. Cierra sesión y vuelve a entrar para aplicar el grupo $MOTOR."
