# Kubernetes (microk8s)

Manifiestos para desplegar los mismos servicios del `docker-compose.yml` en un
clúster de Raspberry Pi con **microk8s**.

```bash
microk8s enable dns storage metrics-server
microk8s kubectl apply -f namespace.yml
microk8s kubectl apply -f api-deployment.yml
```
