# Dockerfile para la aplicación Flask
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY src .
RUN pip install -r requirements.txt

COPY ./src .

# Expone el puerto en el que se ejecutará la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host","0.0.0.0"]
