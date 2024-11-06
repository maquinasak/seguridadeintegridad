FROM python:3.11-slim

WORKDIR /app

# COPY --from=builder /app /app

# Copia los archivos de la aplicación
COPY ./src .

RUN apt update
RUN apt upgrade
RUN apt-get install curl -y
RUN apt-get install iputils-ping -y

# instala los requerimientos
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host","0.0.0.0"]

