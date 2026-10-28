# Registro de uso de IA (Vibe Coding)

Bitácora de trazabilidad exigida por el punto 3 del
[anexo de ética](etica_vibecoding.md). Cada uso relevante de un asistente de IA en el
proyecto se registra aquí.

| Fecha | Herramienta | Objetivo | Prompt (resumen) | Resultado | Validación humana |
|---|---|---|---|---|---|
| 2026-10-27 | Asistente IA | Redactar estructura base del repositorio | "Genera la estructura de carpetas y el README" | Estructura + README | Revisado y ajustado por el equipo |
| 2026-10-27 | Asistente IA | Redactar `docker-compose.yml` inicial | "Compose con Jupyter, API y Ollama, ARM64, sin privilegios" | YAML inicial | Verificado en el Pi; se ajustaron límites de memoria |
| 2026-10-27 | Asistente IA | Guion del primer avance | "Esquema de presentación de 10 minutos" | Guion | Ajustado al tiempo asignado |

## Criterios de registro

1. Se registra todo prompt que produzca código o documentación que llegue al repositorio.
2. Se anota el resultado real, no el esperado.
3. Se indica explícitamente quién validó y qué se corrigió.
4. Los prompts descartados que aporten aprendizaje también se registran.
