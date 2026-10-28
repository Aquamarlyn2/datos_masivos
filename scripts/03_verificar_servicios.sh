#!/usr/bin/env bash
# Comprueba que la pila responde y que el aislamiento está aplicado.
# Uso: bash scripts/03_verificar_servicios.sh
set -uo pipefail

fallo=0

echo "==> Sonda de salud de la API"
if curl -sf http://localhost:8000/health | jq .; then
  echo "    OK"
else
  echo "    FALLO: la API no responde"; fallo=1
fi

echo "==> JupyterLab"
curl -sf -o /dev/null -w "    HTTP %{http_code}\n" http://localhost:8888 || { echo "    FALLO"; fallo=1; }

echo "==> Agente / LLM local"
curl -sf http://localhost:11434/api/tags >/dev/null && echo "    OK" || { echo "    FALLO"; fallo=1; }

echo "==> Aislamiento: ¿el contenedor corre como root?"
uid_api="$(docker exec dm-api id -u 2>/dev/null || echo desconocido)"
echo "    UID en dm-api: $uid_api"
[[ "$uid_api" == "0" ]] && { echo "    FALLO: corre como root"; fallo=1; }

echo "==> Capacidades efectivas del contenedor"
docker exec dm-api grep CapEff /proc/1/status 2>/dev/null | sed 's/^/    /'

echo "==> Red interna sin salida a Internet (ia)"
docker exec dm-ollama sh -c 'timeout 3 wget -q -O- https://example.com' 2>/dev/null \
  && { echo "    FALLO: la red ia tiene salida"; fallo=1; } \
  || echo "    OK: sin salida, como se esperaba"

echo "==> Térmica y throttling"
vcgencmd measure_temp | sed 's/^/    /'
vcgencmd get_throttled | sed 's/^/    /'

echo
[[ $fallo -eq 0 ]] && echo "TODO CORRECTO." || echo "HAY FALLOS: revisa los mensajes anteriores."
exit $fallo
