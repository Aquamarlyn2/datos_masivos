# `monitoring/` — Monitoreo en producción

Herramientas y scripts para vigilar el modelo y los servicios en producción.

| Archivo | Función |
|---|---|
| `prometheus.yml` | Configuración de *scraping* de métricas |
| `alertas.yml` | Reglas de alerta |
| `chequeo_deriva.py` | Detección de deriva (*data drift*) |
| `panel_salud.sh` | Resumen rápido del estado del Pi |

Las métricas cumplen dos funciones: **rendimiento** (latencia, deriva) y
**seguridad** (consumo anómalo de CPU/memoria, disco lleno). Ver
[docs/seguridad.md](../docs/seguridad.md#5-observabilidad-como-control-de-seguridad).
