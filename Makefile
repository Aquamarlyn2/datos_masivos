.PHONY: ayuda preparar contenedores levantar verificar pruebas entrenar predecir limpiar

ayuda:
	@echo "Objetivo                      Descripción"
	@echo "preparar                      Optimiza y endurece el host"
	@echo "contenedores                  Instala Docker/Podman"
	@echo "levantar                      Despliega la pila de servicios"
	@echo "verificar                     Comprueba que todo responde"
	@echo "pruebas                       Ejecuta la batería de pruebas"
	@echo "entrenar                      Entrena el modelo"
	@echo "predecir                      Consulta la API de inferencia"

preparar:
	sudo bash scripts/00_preparar_host.sh

contenedores:
	bash scripts/01_instalar_contenedores.sh

levantar:
	bash scripts/02_levantar_servicios.sh

verificar:
	bash scripts/03_verificar_servicios.sh

pruebas:
	bash scripts/06_validar_pruebas.sh

entrenar:
	bash scripts/04_entrenar_modelo.sh

predecir:
	bash scripts/05_ejecutar_predicciones.sh

limpiar:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov
