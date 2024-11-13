
FROM python:3.11-slim
# FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
# Update package lists and install OpenSSL
RUN apt-get update 
RUN apt-get install -y openssl 
RUN apt-get install openssh-client -y
RUN apt-get install -y curl 
RUN apt-get install curl -y
RUN apt-get install iputils-ping -y
RUN pip install --upgrade pip

RUN apt-get install procps -y
RUN apt-get update && apt-get install -y passwd

ENV ROOT_PASSWORD ladesiempre123456
RUN echo "root:${ROOT_PASSWORD}" | chpasswd

RUN rm -rf /var/lib/apt/lists/*  

WORKDIR /app


# Copia los archivos de la aplicación
COPY ./src .

# instala los requerimientos
RUN pip install -r requirements.txt

#elimino las claves generadas
RUN rm cert.pem key.pem
RUN rm host_ed25519_key.pem

# RUN openssl req -x509 -new -nodes -config openssl.cnf -out server.crt -keyout server.key
RUN openssl req -x509 -newkey rsa:4096 -nodes -config openssl.cnf -out cert.pem -keyout key.pem


# Generate an RSA private key (2048 bits)
RUN openssl genpkey -algorithm RSA -out host_rsa_key.pem -pkeyopt rsa_keygen_bits:2048

# Generate the public key corresponding to the private key
RUN openssl rsa -in host_rsa_key.pem -pubout -out host_rsa_key.pub

# Generate an ECDSA private key (256 bits, 384 bits, or 521 bits can be used)
RUN openssl ecparam -name prime256v1 -genkey -noout -out host_ecdsa_key.pem

# Generate the public key corresponding to the private key
RUN openssl ec -in host_ecdsa_key.pem -pubout -out host_ecdsa_key.pub

# Generate ED25519 key using ssh-keygen
RUN ssh-keygen -t ed25519 -f host_ed25519_key.pem -N ""





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

