# Investigación: sistema operativo Linux optimizado para Raspberry Pi 5

## 1. Selección del sistema operativo

### Criterios de evaluación

| Criterio | Peso | Razón |
|---|---|---|
| Soporte ARM64 nativo | Alto | El Pi 5 es **aarch64**; emular x86 es inviable en rendimiento |
| Soporte oficial del hardware | Alto | GPIO, PCIe/NVMe, cámara, *thermal management* |
| Ligereza (sin escritorio) | Alto | 16 GB se reservan para cargas de datos e IA |
| Soporte de contenedores | Alto | cgroups v2, namespaces, seccomp, AppArmor |
| Ecosistema y documentación | Medio | Facilita resolver incidencias |
| Estabilidad a largo plazo | Medio | Menos mantenimiento |

### Comparativa

| Distribución | Kernel | Contenedores | Ventajas | Inconvenientes |
|---|---|---|---|---|
| **Raspberry Pi OS Lite 64-bit (Bookworm)** | 6.6 LTS propio | Docker / Podman | Soporte oficial total, mínimo consumo, 16K pages | Repos algo conservadores |
| Ubuntu Server 24.04 LTS ARM64 | 6.8 | Docker / Podman | Documentación enorme, 5 años de soporte | Más peso, *snapd* consume recursos |
| Fedora IoT | 6.x reciente | Podman nativo (rootless por defecto) | Inmutable, muy seguro, *rpm-ostree* | Curva de aprendizaje |
| openSUSE MicroOS | 6.x | Podman / k3s | Actualizaciones atómicas y reversibles | Menos ejemplos en español |
| Alpine Linux | 6.x | Docker / Podman | Extremadamente ligero | *musl* complica algunas dependencias de Python |

### Decisión

Se elige **Raspberry Pi OS Lite 64-bit** como sistema base:

1. Es la distribución con **mejor soporte del hardware** del Pi 5 (firmware, NVMe, térmica).
2. La variante **Lite** no carga escritorio, liberando RAM para los contenedores.
3. Su kernel 6.6 LTS ya incluye los **cgroups v2** y los *namespaces* necesarios.
4. Está basada en Debian, por lo que el ecosistema de paquetes y guías es amplio.

> Como alternativa documentada: Ubuntu Server 24.04 ARM64 si se requiere soporte
> empresarial a 5 años.

---

## 2. Optimización del kernel de Linux

### 2.1 Habilitar cgroups de memoria

Sin esto, no se pueden imponer límites de memoria a los contenedores. En
`/boot/firmware/cmdline.txt` (todo en una sola línea):

```text
console=serial0,115200 console=tty1 root=PARTUUID=xxxx rootfstype=ext4 fsck.repair=yes rootwait cgroup_enable=memory cgroup_memory=1
```

Verificación:

```bash
cat /proc/cgroups | grep memory
cat /sys/fs/cgroup/cgroup.controllers
```

### 2.2 Páginas de 16 KB

El kernel de Raspberry Pi OS para Pi 5 usa páginas de **16 KB**, lo que reduce la
presión sobre la TLB y mejora el rendimiento en cargas de acceso a memoria
(entrenamiento de modelos, *dataframes* grandes). Se comprueba con:

```bash
getconf PAGESIZE    # debe devolver 16384
```

### 2.3 Parámetros de red y arranque

En `/etc/sysctl.d/99-datos-masivos.conf`:

```ini
# Cola de conexiones para APIs de inferencia
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 2048
# Menos swap agresivo: priorizamos RAM
vm.swappiness = 10
# Más descriptores de archivo para Jupyter y workers
fs.file-max = 2097152
```

### 2.4 Almacenamiento NVMe (crítico)

La microSD es el cuello de botella del Pi 5. Se recomienda NVMe por HAT PCIe:

```ini
# /boot/firmware/config.txt
dtparam=pciex1
dtparam=pciex1_gen=3
```

### 2.5 Gestión térmica

El Pi 5 reduce frecuencia a partir de 80 °C. Se instala el disipador activo oficial y
se verifica:

```bash
vcgencmd measure_temp
vcgencmd get_throttled     # 0x0 = sin throttling
```

### 2.6 Servicios innecesarios

```bash
sudo systemctl disable --now bluetooth hciuart avahi-daemon cups triggerhappy
```

---

## 3. Compatibilidad de imágenes ARM64

Toda imagen usada en `deployment/docker-compose.yml` debe publicar
`linux/arm64`. Verificación:

```bash
docker manifest inspect quay.io/jupyter/scipy-notebook:latest | grep architecture
```

| Servicio | Imagen | ARM64 |
|---|---|---|
| Jupyter | `quay.io/jupyter/scipy-notebook` | ✅ |
| API de inferencia | `python:3.12-slim` (base propia) | ✅ |
| Agente / LLM local | `ollama/ollama` | ✅ |
| Base de datos | `postgres:16-alpine` | ✅ |
| Métricas | `prom/prometheus`, `grafana/grafana` | ✅ |

Si una imagen no soporta ARM64, las alternativas son: (a) buscar una equivalente
nativa, (b) construirla desde `Dockerfile` en `deployment/`, o (c) descartarla —
**nunca** recurrir a emulación QEMU en producción.
