# `deployment/` — Despliegue

Scripts y configuraciones para desplegar el modelo y los servicios.

| Ruta | Contenido |
|---|---|
| `docker-compose.yml` | Pila completa de microservicios (ARM64) |
| `.env.example` | Plantilla de variables secretas |
| `api/Dockerfile` | Imagen de la API de inferencia |
| `ansible/` | Aprovisionamiento reproducible del host |
| `terraform/` | Infraestructura como código (para escalar a clúster) |
| `k8s/` | Manifiestos de Kubernetes (microk8s en el Pi) |

## Uso

```bash
cp .env.example .env      # completar secretos
docker compose up -d
docker compose ps
```
