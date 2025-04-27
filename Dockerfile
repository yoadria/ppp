# Usa una imagen de Python liviana
FROM python:3.12.3-slim

# Define el directorio de trabajo
WORKDIR /ppp

# Copia tu proyecto dentro del contenedor
COPY . .

# Instala las librerías necesarias
RUN pip install --no-cache-dir -r /ppp/requirements.txt

# Expone el puerto de Flask
EXPOSE 5000

# Comando para correr l app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
