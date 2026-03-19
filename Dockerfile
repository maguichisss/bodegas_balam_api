# Usa una imagen base de Python
FROM python:3.10-slim
# Establece el directorio de trabajo
WORKDIR /app
# Copia los requerimientos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copia el resto del código de la aplicación
COPY ./app ./app
# Comando para ejecutar la aplicación (ajusta según tu estructura)
# uvicorn bb_backend.app.main:app --host 0.0.0.0 --port 8000
# Nota: Como estamos dentro de la carpeta bb_backend, el PYTHONPATH ya incluye el directorio actual.
# Asegúrate de que la estructura de imports en main.py sea relativa a app/.
# Si main.py está en bb_backend/app/main.py, y WORKDIR es /app, entonces el comando es:
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
