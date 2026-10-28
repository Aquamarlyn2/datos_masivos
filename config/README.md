# `config/` — Configuración

Archivos de configuración del proyecto, incluyendo la configuración de logs.

| Archivo | Función |
|---|---|
| `logging.yml` | Configuración de logs con rotación |
| `postgresql.conf` | Ajustes de PostgreSQL para 16 GB de RAM |
| `parametros.yml` | Parámetros del proyecto y de los modelos |

> Las **credenciales** no viven aquí: van en `deployment/.env`, que está
> excluido del control de versiones.
