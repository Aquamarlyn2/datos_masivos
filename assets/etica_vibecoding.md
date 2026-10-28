# Ética en el uso de "Vibe Coding"

Este documento es el **anexo de ética** del proyecto. Define las reglas con las que el
equipo utiliza asistentes de IA (Vibe Coding) para generar código. La IA es una
**herramienta auxiliar**: la responsabilidad técnica y ética del resultado es siempre humana.

---

## 1. Validación humana

Usar Vibe Coding como herramienta auxiliar para generar código, pero **validar siempre
los resultados manualmente** para evitar sesgos o errores en pipelines de datos.

- Ningún fragmento generado se integra a `src/` o `pipelines/` sin revisión.
- Toda contribución asistida por IA pasa por *pull request* y revisión de al menos otra persona.

## 2. Cumplimiento normativo y privacidad

Cumplir con las normativas aplicables, como la **anonimización de datos sensibles**
antes de cualquier automatización.

- Ningún dataset con datos personales entra a `notebooks/` o `pipelines/` sin anonimizar.
- Se documenta la base legal y el fin del tratamiento en `config/`.

## 3. Trazabilidad y explicabilidad

**Registrar prompts, generaciones de IA y modificaciones** para auditorías, permitiendo
explicabilidad en modelos de datos.

- Bitácora pública en [`registro_prompts.md`](registro_prompts.md).
- Cada commit asistido por IA referencia la entrada correspondiente de la bitácora.

## 4. Despliegue responsable

**No desplegar código generado sin validaciones manuales** en etapas clave, como
entrenamiento de modelos o inferencia.

- La promoción a `models/` requiere pruebas en `tests/` y validación en el *staging*.

## 5. Equidad y sesgo

**Evaluar datasets y outputs por equidad**; ajustar los prompts para favorecer la
diversidad en el análisis de datos.

- Revisiones de sesgo documentadas por cada modelo promovido.
- Métricas desagregadas por subgrupo cuando aplique.

## 6. Automatización con criterio

**Automatizar solo procesos no críticos**; reservar el juicio humano para decisiones de
impacto ético o social.

- Los `pipelines/` pueden automatizar ETL y entrenamiento.
- Las decisiones con efecto sobre personas requieren aprobación explícita.

## 7. Seguridad

**Escanear el código por vulnerabilidades** y realizar *modelado de amenazas* antes de
llevarlo a producción en flujos de datos.

- Análisis estático (SAST) y escaneo de dependencias en `ci-cd/`.
- Escaneo de imágenes de contenedor con Trivy antes de cada despliegue.
- Modelado de amenazas documentado en `docs/seguridad.md`.

## 8. Límites claros para la IA

**Definir límites claros para la IA en el equipo**, con métricas de observabilidad y
despliegues graduales.

- La IA no tiene acceso a producción ni a credenciales.
- Todo servicio expone métricas consumidas por `monitoring/`.

## 9. Derechos humanos y sostenibilidad

**Evitar restricciones a los derechos humanos**; optimizar para un bajo consumo
energético en computación intensiva.

- Cargas de trabajo dimensionadas para el presupuesto térmico y eléctrico del Pi 5.
- Preferencia por modelos pequeños y cuantizados (Q4) para inferencia local.

## 10. Aprendizaje responsable

**Revisar y entrenar continuamente prompts y modelos con retroalimentación**,
priorizando el aprendizaje responsable.

- Retrospectivas periódicas sobre qué prompts funcionaron y cuáles introdujeron errores.
- Actualización de esta política conforme evoluciona el proyecto.

---

## Referencias

- Documento base del curso: `datos_masivos/assets/etica_vibecoding.md`
- Principios de IA responsable aplicados al ciclo de vida de datos y modelos.
