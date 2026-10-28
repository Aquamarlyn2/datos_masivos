# `pipelines/` — Canalizaciones

Orquestación de las etapas del ciclo de vida de los datos y los modelos.

```text
pipelines/
├── preprocesamiento_pipeline.py   Datos crudos → dataset limpio
├── entrenamiento_pipeline.py      Dataset limpio → modelo
└── prediccion_pipeline.py         Modelo + datos nuevos → predicciones
```

Cada pipeline es idempotente y registra su ejecución en `config/logs/`, lo que
permite auditar qué versión de datos produjo qué versión de modelo.
