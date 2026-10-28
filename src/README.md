# `src/` — Código fuente

Código del proyecto, validado manualmente antes de integrarse
(ver [anexo de ética](../assets/etica_vibecoding.md)).

```text
src/
├── preprocesamiento/     Limpieza y transformación de datos
├── caracteristicas/      Ingeniería de características
├── modelos/              Definición y entrenamiento de modelos
├── visualizacion/        Gráficas y reportes
├── api/                  API de inferencia (FastAPI)
└── utils/                Funciones auxiliares
```

## Convenciones

- Un módulo por responsabilidad; nada de lógica de negocio en los notebooks.
- Type hints y docstrings en funciones públicas.
- Cobertura de pruebas mínima del 80 % antes de promover a `models/`.
