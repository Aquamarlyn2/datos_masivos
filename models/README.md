# `models/` — Modelos entrenados

Almacena los modelos entrenados junto con sus hiperparámetros.

## Convención

```text
models/
├── modelo_rf.joblib          Pesos del modelo
├── modelo_rf.json            Hiperparámetros, métricas y sello de tiempo
└── historial.md              Registro de versiones promovidas
```

## Reglas

1. **Ningún modelo se promueve sin validación manual** (anexo de ética, punto 4).
2. Cada modelo guardado se acompaña de sus métricas y de la fecha de entrenamiento.
3. Los artefactos grandes se versionan con Git LFS o se regeneran desde `pipelines/`.
