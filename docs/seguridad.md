# Mejores prácticas de seguridad

Documento de referencia del punto 7 del [anexo de ética](../assets/etica_vibecoding.md)
(escaneo de vulnerabilidades y modelado de amenazas).

---

## 1. Modelado de amenazas (STRIDE)

| Amenaza | Escenario en este proyecto | Mitigación |
|---|---|---|
| **S**poofing | Acceso SSH con contraseña | Solo llaves Ed25519, sin `root` |
| **T**ampering | Imagen de contenedor alterada | Fijar *digest*, escaneo con Trivy |
| **R**epudiation | No saber qué código generó la IA | Bitácora de prompts |
| **I**nformation disclosure | Secrets en el YAML | `.env` + `secrets`, `.gitignore` |
| **D**enial of service | Un contenedor consume toda la RAM | Límites de CPU/memoria, cgroups v2 |
| **E**levation of privilege | Contenedor `--privileged` | `cap_drop: ALL`, usuario no root, rootless |

---

## 2. Endurecimiento del sistema base

```bash
# SSH: sin contraseñas, sin root directo
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# Firewall: denegar todo por defecto
sudo apt install -y ufw fail2ban unattended-upgrades
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable

# Actualizaciones automáticas de seguridad
sudo dpkg-reconfigure -plow unattended-upgrades
```

| Medida | Herramienta | Estado |
|---|---|---|
| Solo llaves SSH | `sshd_config` | Aplicado |
| Firewall con deny por defecto | `ufw` | Aplicado |
| Bloqueo de fuerza bruta | `fail2ban` | Aplicado |
| Actualizaciones automáticas | `unattended-upgrades` | Aplicado |
| Montaje `/tmp` con `noexec` | `/etc/fstab` | Recomendado |

---

## 3. Endurecimiento de contenedores

Principios aplicados a **todo** servicio en `deployment/docker-compose.yml`:

1. **Rootless** — Podman sin privilegios, o Docker como usuario del grupo `docker`
   con `userns-remap`.
2. **Nunca `--privileged`** y nunca montar el socket de Docker dentro de un contenedor.
3. **`cap_drop: [ALL]`** y añadir solo la capacidad estrictamente necesaria.
4. **`no-new-privileges:true`** para impedir la escalada vía *setuid*.
5. **Sistema de archivos de solo lectura** + `tmpfs` para lo que deba escribirse.
6. **Usuario no root** dentro de la imagen.
7. **Límites de recursos** (CPU y memoria) para evitar DoS.
8. **Redes separadas** por servicio; solo se publican los puertos necesarios.
9. **`restart: unless-stopped`**, límite de logs y rotación en `config/`.
10. **Escaneo con Trivy** antes de cada despliegue:

```bash
trivy image --severity HIGH,CRITICAL quay.io/jupyter/scipy-notebook:latest
```

11. **Secrets fuera del repositorio**: `.env` (ignorado por Git) o Docker secrets.
12. **Perfiles AppArmor** aplicados a los servicios expuestos.

---

## 4. Seguridad en el ciclo de vida de los datos y modelos

- Anonimización **antes** de cualquier automatización (punto 2 del anexo de ética).
- Cifrado en reposo del volumen de datos cuando contenga información sensible.
- Cifrado en tránsito: TLS terminado por un *reverse proxy* (Caddy/Traefik).
- Versionado de modelos en `models/` con hash y métricas asociadas.
- Registro de auditoría de inferencias para trazabilidad.

---

## 5. Observabilidad como control de seguridad

`monitoring/` expone métricas que también son señales de seguridad:

| Métrica | Señal |
|---|---|
| `container_memory_usage_bytes` | Posible fuga de memoria o DoS |
| `container_cpu_usage_seconds_total` | Minado o procesos anómalos |
| `node_filesystem_avail_bytes` | Disco lleno por logs no rotados |
| `vcgencmd get_throttled` (exportado) | Degradación térmica sostenida |
