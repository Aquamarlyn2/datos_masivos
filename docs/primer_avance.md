# Guion del primer avance

**Fecha:** 9 de noviembre de 2026, 13:00 h — sesión virtual.

## Objetivo de la sesión

Demostrar que el entorno quedó **instalado, optimizado y endurecido**, y que los
contenedores de ciencia de datos y agentes corren sobre él.

## Orden de la presentación (10–12 min)

### 1. Contexto y objetivo (1 min)
- Raspberry Pi 5 (16 GB) como plataforma de microservicios de datos e IA.
- El reto real: ARM64, 16 GB de RAM y un presupuesto térmico limitado.

### 2. Sistema operativo elegido (2 min)
- Raspberry Pi OS Lite 64-bit frente a las alternativas
  ([investigacion.md](investigacion.md#1-selección-del-sistema-operativo)).
- Optimizaciones del kernel: cgroups de memoria, páginas de 16 KB, `vm.swappiness`,
  NVMe por PCIe.

### 3. Seguridad (3 min)
- Modelado de amenazas STRIDE ([seguridad.md](seguridad.md#1-modelado-de-amenazas-stride)).
- Host: SSH con llave, ufw, fail2ban, actualizaciones automáticas.
- Contenedores: sin privilegios, `cap_drop: ALL`, solo lectura, límites de recursos,
  escaneo con Trivy.

### 4. Demostración en vivo (4 min)
```bash
# Estado del sistema
getconf PAGESIZE; vcgencmd measure_temp; vcgencmd get_throttled

# Contenedores en ejecución
docker compose -f deployment/docker-compose.yml ps

# Aislamiento demostrado
docker exec api whoami                     # usuario no root
docker exec api cat /proc/1/status | head  # capacidades reducidas

# Escaneo de seguridad
trivy image --severity HIGH,CRITICAL quay.io/jupyter/scipy-notebook:latest

# Servicio funcionando
curl http://localhost:8000/health
```

### 5. Estructura y documentación (1 min)
- Recorrido por las carpetas del repositorio.
- Todo en Markdown, contenedores en YAML.

### 6. Anexo de ética (1 min)
- Política de uso de "Vibe Coding" y bitácora de prompts.

### 7. Cierre y siguientes pasos (1 min)
- `pipelines/` completo, CI/CD en GitLab, Kubernetes/Terraform, monitoreo con alertas.

---

## Lista de verificación previa

- [ ] Repositorio con la estructura completa, cada carpeta con su `README.md`
- [ ] `README.md` raíz con objetivo y guía de inicio
- [ ] `docs/investigacion.md` con la comparativa de SO
- [ ] `docs/seguridad.md` con el modelo de amenazas
- [ ] `deployment/docker-compose.yml` funcional en ARM64
- [ ] `assets/etica_vibecoding.md` presente
- [ ] `assets/registro_prompts.md` con la bitácora
- [ ] Raspberry Pi encendida, con los contenedores corriendo
- [ ] Prueba de la demostración en vivo, ejecutada al menos una vez
