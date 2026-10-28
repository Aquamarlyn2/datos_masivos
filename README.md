# datos_masivos — Raspberry Pi 5 como plataforma de microservicios de ciencia de datos

Proyecto de investigación e implementación: preparar una **Raspberry Pi 5 (16 GB)**
con un sistema operativo Linux optimizado para ejecutar **contenedores seguros**
orientados a ciencia de datos y agentes computacionales inteligentes.

---

## Objetivo

Investigar e implementar un sistema operativo con kernel Linux optimizado que permita
configurar contenedores siguiendo mejores prácticas de seguridad, para ejecutar
microservicios orientados a ciencia de datos y agentes computacionales inteligentes
sobre Raspberry Pi 5 (16 GB).

## Alcance

| Entregable | Descripción | Estado |
|---|---|---|
| Estructura del repositorio | Carpetas según la mejor práctica indicada | ✅ |
| Investigación de SO | Comparativa de distribuciones ARM64 + optimización de kernel | ✅ |
| Endurecimiento (hardening) | Sistema base y runtime de contenedores | ✅ |
| Contenedores | Orquestación con Docker Compose / Podman Compose (YAML) | ✅ |
| Microservicios | Jupyter, API de inferencia, agente inteligente | ✅ |
| Documentación | Todo en Markdown | ✅ |
| Anexo de ética | Política de uso de "Vibe Coding" | ✅ |

---

## Hardware

- **Raspberry Pi 5, 16 GB de RAM** (arquitectura **ARM64 / aarch64**)
- Almacenamiento NVMe por HAT PCIe (recomendado) o SSD USB 3.0
- Fuente oficial de 27 W (5 V / 5 A) — obligatoria para el Pi 5
- Disipador activo oficial (el Pi 5 hace *throttling* sin ventilación)

> ⚠️ **Nota crítica sobre arquitectura:** la Raspberry Pi 5 es **ARM64**, no x86-64.
> Toda imagen de contenedor debe publicar manifiesto `linux/arm64`. Ver
> [docs/investigacion.md](docs/investigacion.md#compatibilidad-de-imágenes-arm64).

---

## Sistema operativo elegido

**Raspberry Pi OS Lite 64-bit (Bookworm)** — ver justificación completa en
[docs/investigacion.md](docs/investigacion.md#1-selección-del-sistema-operativo).

---

## Inicio rápido

```bash
# 1. Clonar
git clone https://github.com/edgarOswaldoDiaz/datos_masivos.git
cd datos_masivos

# 2. Preparar el host (una sola vez)
sudo bash scripts/00_preparar_host.sh

# 3. Levantar la pila de servicios
bash scripts/02_levantar_servicios.sh

# 4. Verificar
bash scripts/03_verificar_servicios.sh
```

---

## Estructura del repositorio

```text
datos_masivos/
├── assets/         Archivos estáticos: imágenes, documentos, política de ética
├── config/         Configuración del proyecto, incluyendo logs
├── notebooks/      Notebooks de Jupyter: exploración, preprocesamiento, entrenamiento y evaluación
├── src/            Código fuente: preprocesamiento, ingeniería de características, modelos, visualización
├── tests/          Pruebas unitarias y de integración
├── scripts/        Scripts de automatización: validación, entrenamiento, predicciones, despliegue
├── pipelines/      Canalizaciones de preprocesamiento, entrenamiento y predicciones
├── deployment/     Scripts y configuraciones de despliegue (Docker, Kubernetes, Terraform, Ansible)
├── monitoring/     Scripts y herramientas de monitoreo del modelo en producción
├── ci-cd/          Integración continua y despliegue continuo (GitLab CI)
├── frontend/       Código del front-end del proyecto (Webpack)
├── models/         Modelos entrenados y sus hiperparámetros
└── docs/           Documentación en Markdown
```

---

## Documentación

| Documento | Contenido |
|---|---|
| [docs/investigacion.md](docs/investigacion.md) | Comparativa de SO, optimización del kernel |
| [docs/seguridad.md](docs/seguridad.md) | Endurecimiento del kernel, contenedores y microservicios |
| [docs/arquitectura.md](docs/arquitectura.md) | Diagrama y descripción de la topología |
| [docs/instalacion.md](docs/instalacion.md) | Guía de instalación paso a paso |
| [docs/primer_avance.md](docs/primer_avance.md) | Guion para la sesión del 9 de noviembre de 2026 |
| [assets/etica_vibecoding.md](assets/etica_vibecoding.md) | **Anexo:** Ética en el uso de "Vibe Coding" |

---

## Fechas

- **Primer avance:** 9 de noviembre de 2026, 13:00 h — sesión virtual.

## Licencia

Uso académico. Ver `LICENSE`.
