
FROM python:3.11-slim
# FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
# Update package lists and install OpenSSL
RUN apt-get update 
RUN apt-get install -y openssl 
RUN apt-get install -y curl 
RUN apt-get install curl -y
RUN apt-get install iputils-ping -y
RUN pip install --upgrade pip

RUN rm -rf /var/lib/apt/lists/*  

WORKDIR /app


# Copia los archivos de la aplicación
COPY ./src .

# instala los requerimientos
RUN pip install -r requirements.txt

# RUN openssl req -x509 -new -nodes -config openssl.cnf -out server.crt -keyout server.key
RUN rm cert.pem key.pem
RUN openssl req -x509 -newkey rsa:4096 -nodes -config openssl.cnf -out cert.pem -keyout key.pem

# RUN openssl req -x509 -nodes -days 365 -config openssl.cnf -newkey rsa:2048 -keyout server.key -out server.crt

# Create a new user and group
RUN groupadd -r flaskgroup 
RUN useradd -r flaskuser -g flaskgroup

# Give the new user ownership of the /app directory
RUN chown -R flaskuser:flaskgroup /app

# Restrict permissions for the /app folder to the flaskuser only
RUN chmod -R 750 /app

# Switch to the new user
USER flaskuser

EXPOSE 443
# EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host","0.0.0.0"]

