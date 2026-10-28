# `scripts/` — Automatización

Scripts para tareas concretas: validación de pruebas, entrenamiento,
predicciones y despliegue. Se ejecutan en este orden en una instalación limpia.

| Script | Función |
|---|---|
| `00_preparar_host.sh` | Optimiza y endurece el sistema base |
| `01_instalar_contenedores.sh` | Instala Docker/Podman y Trivy |
| `02_levantar_servicios.sh` | Despliega la pila de contenedores |
| `03_verificar_servicios.sh` | Comprueba que todo responde |
| `04_entrenar_modelo.sh` | Entrena y guarda el modelo |
| `05_ejecutar_predicciones.sh` | Consulta la API de inferencia |
| `06_validar_pruebas.sh` | Corre la batería de pruebas |
