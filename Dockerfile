# Usa una imagen de Python liviana
FROM python:3.12.3-slim

# Define el directorio de trabajo
WORKDIR /app

# Copia tu proyecto dentro del contenedor
COPY . /ppp

# Instala las librerías necesarias
RUN pip install --no-cache-dir -r /ppp/requirements.txt

# Expone el puerto de Flask
EXPOSE 5000

# Comando para correr Flask
CMD ["python", "/ppp/main.py"]
