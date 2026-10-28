# Imagen de la API de inferencia — linux/arm64
FROM python:3.12-slim

# Usuario sin privilegios
RUN groupadd -g 1000 app && useradd -m -u 1000 -g app app

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/
COPY config/ /app/config/

USER 1000:1000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
