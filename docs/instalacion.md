# Guía de instalación paso a paso

## 0. Materiales

- Raspberry Pi 5 (16 GB) + fuente oficial de 27 W + disipador activo
- SSD NVMe con HAT PCIe (recomendado) o microSD Clase A2
- Lector de tarjetas / adaptador NVMe para el grabado inicial
- Otro equipo para grabar la imagen (`rpi-imager`)

## 1. Grabar el sistema operativo

1. Descargar **Raspberry Pi Imager**.
2. Elegir *Raspberry Pi OS (other)* → **Raspberry Pi OS Lite (64-bit)**.
3. En el engranaje de configuración avanzada:
   - Definir `hostname`: `datos-masivos`
   - Usuario y contraseña (temporal; luego se pasa a solo llave)
   - Configurar Wi-Fi y zona horaria
   - **Habilitar SSH**
4. Grabar y arrancar.

## 2. Primer arranque

```bash
ssh usuario@datos-masivos.local
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

## 3. Preparar el host

```bash
sudo bash scripts/00_preparar_host.sh
sudo reboot     # necesario para aplicar cmdline.txt
```

El script aplica: cgroups de memoria, parámetros `sysctl`, ufw, fail2ban,
actualizaciones automáticas y desactivación de servicios no usados.

## 4. Verificar la optimización

```bash
cat /sys/fs/cgroup/cgroup.controllers   # debe incluir "memory"
getconf PAGESIZE                        # 16384
vcgencmd measure_temp
vcgencmd get_throttled                  # 0x0
```

## 5. Instalar el runtime de contenedores

```bash
bash scripts/01_instalar_contenedores.sh
```

Instala Docker Engine + Compose plugin (o Podman + `podman-compose`), añade el
usuario al grupo correspondiente y habilita Trivy.

## 6. Configurar secrets

```bash
cp deployment/.env.example deployment/.env
nano deployment/.env      # definir contraseñas fuertes
```

`.env` está en `.gitignore`: **jamás** se sube al repositorio.

## 7. Levantar los servicios

```bash
bash scripts/02_levantar_servicios.sh
bash scripts/03_verificar_servicios.sh
```

## 8. Accesos

| Servicio | URL | Puerto |
|---|---|---|
| Frontend | http://datos-masivos.local | 3000 |
| JupyterLab | http://datos-masivos.local:8888 | 8888 |
| API (docs) | http://datos-masivos.local:8000/docs | 8000 |
| Ollama | http://datos-masivos.local:11434 | 11434 |
| Grafana | http://datos-masivos.local:3001 | 3001 |

## 9. Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| Los contenedores no arrancan | Falta cgroup de memoria | Revisar `cmdline.txt` y reiniciar |
| `no matching manifest for linux/arm64` | Imagen solo x86 | Buscar alternativa ARM64 |
| El Pi se apaga o va lento | Fuente insuficiente | Usar la fuente oficial de 27 W |
| `get_throttled` ≠ 0x0 | Sobrecalentamiento | Revisar disipador y ventilación |
| Jupyter no ve los notebooks | Ruta del volumen | Verificar `deployment/docker-compose.yml` |
