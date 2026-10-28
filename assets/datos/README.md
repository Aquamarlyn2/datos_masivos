# Datos

- `crudos.csv` — datos de entrada tal como llegan.
- `limpios.parquet` — salida de `pipelines/preprocesamiento_pipeline.py`.
- `nuevos.parquet` — lote para inferencia.
- `predicciones.parquet` — salida de `pipelines/prediccion_pipeline.py`.

> ⚠️ Los datos con información personal **no se suben al repositorio** hasta estar
> anonimizados (anexo de ética, punto 2). Los archivos de datos están en `.gitignore`.
