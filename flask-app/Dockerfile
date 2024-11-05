
FROM python:3.11-slim
# FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
# Update package lists and install OpenSSL
RUN apt-get update 
RUN apt-get install -y openssl 
RUN apt-get install -y curl 
# RUN apt-get install -y python3 python3-pip
RUN rm -rf /var/lib/apt/lists/*  

WORKDIR /app

RUN pip install --upgrade pip

# Copia los archivos de la aplicación
COPY ./src .


# instala los requerimientos
RUN pip install -r requirements.txt


# RUN openssl req -x509 -new -nodes -config openssl.cnf -out server.crt -keyout server.key
RUN rm cert.pem key.pem
RUN openssl req -x509 -newkey rsa:4096 -nodes -config openssl.cnf -out cert.pem -keyout key.pem

# RUN openssl req -x509 -nodes -days 365 -config openssl.cnf -newkey rsa:2048 -keyout server.key -out server.crt


EXPOSE 443
# EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
# CMD ["flask", "run", "--host","0.0.0.0"]

