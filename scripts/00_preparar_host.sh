#!/usr/bin/env bash
# Optimiza y endurece el sistema base de la Raspberry Pi 5.
# Uso: sudo bash scripts/00_preparar_host.sh
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Ejecutar con sudo." >&2
  exit 1
fi

echo "==> 1/7 Habilitando cgroups de memoria"
CMDLINE=/boot/firmware/cmdline.txt
if ! grep -q "cgroup_enable=memory" "$CMDLINE"; then
  cp "$CMDLINE" "${CMDLINE}.bak"
  sed -i 's/$/ cgroup_enable=memory cgroup_memory=1/' "$CMDLINE"
  echo "    Añadido a cmdline.txt (requiere reinicio)"
else
  echo "    Ya estaba habilitado"
fi

echo "==> 2/7 Parámetros del kernel"
cat > /etc/sysctl.d/99-datos-masivos.conf <<'EOF'
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 2048
vm.swappiness = 10
fs.file-max = 2097152
EOF
sysctl --system >/dev/null

echo "==> 3/7 Paquetes de seguridad"
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  ufw fail2ban unattended-upgrades trivy jq >/dev/null

echo "==> 4/7 Cortafuegos"
ufw --force default deny incoming >/dev/null
ufw --force default allow outgoing >/dev/null
ufw allow 22/tcp >/dev/null
ufw allow 3000/tcp >/dev/null   # frontend
ufw allow 3001/tcp >/dev/null   # grafana
ufw --force enable >/dev/null

echo "==> 5/7 SSH sin contraseñas"
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart ssh

echo "==> 6/7 Servicios innecesarios"
for svc in bluetooth hciuart avahi-daemon cups triggerhappy; do
  systemctl disable --now "$svc" 2>/dev/null || true
done

echo "==> 7/7 Actualizaciones automáticas"
dpkg-reconfigure -plow unattended-upgrades >/dev/null 2>&1 || true

echo
echo "LISTO. Reinicia para aplicar los cgroups:  sudo reboot"
