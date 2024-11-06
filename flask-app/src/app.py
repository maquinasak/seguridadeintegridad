from flask import Flask, request, jsonify, send_from_directory, session
import mysql.connector
import subprocess
import bcrypt
import jwt
from datetime import datetime, timedelta


# Replace with your desired secret key
SECRET_KEY = 'lasuertedelprincipiantenopuedefallar'

app = Flask(__name__,static_folder='static')

# MySQL connection details
db_host = "mysql"
db_user = "user"
db_password = "password"
db_name = "mydatabase"

# Function to connect to the database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def generate_jwt_token(user_id):
    """Generates a JWT token for a given user ID."""
    ahora = datetime.now()
    expiration_time =  ahora + timedelta(minutes=30)

    # Create the token payload
    payload = {
        'exp': expiration_time,
        'user_id': user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(hashed_password, plain_password):
    """Verifies if the plain password matches the hashed password."""
    # return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password)
    rdo = bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))
    return rdo

# # Endpoint to create a new usuario
# @app.route('/', methods=['GET'])
# def inicio():
#     return jsonify({'message': 'Inicio correcto'}), 200

@app.route('/')
def serve_index():
    # return jsonify({'message': 'llegué..'}), 200
    return send_from_directory('static', 'index.html')
    # return app.send_static_file('static/index.html')

@app.route('/ingresar')
def serve_login():
    # return jsonify({'message': 'llegué..'}), 200
    return send_from_directory('static', 'login.html')
    # return app.send_static_file('static/index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    contrasenia = data.get('contrasenia')

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM usuarios where email = %s"
    val = (email, )
    cursor.execute(sql, val)
    usuarios = cursor.fetchone()

    data = {
        "rta":"ok",
        "result": usuarios
    }

    if len(usuarios)>0:
        hashed_password = usuarios[4]
        if verify_password(hashed_password, contrasenia):
            token = generate_jwt_token(email)
            access_token = generate_jwt_token(email)
            token = access_token
            if not 'username' in session:
                session['username'] = email
        
            return jsonify({'token': token}),200 
        else:
            return jsonify({'error': 'Invalid password', 'hashed_password':hashed_password,'plin':contrasenia}), 401
    else:
        return jsonify({'error': 'incorrect credentials'}), 404


# Endpoint to create a new usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    email = data.get('email')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fechanac = data.get('fechanac')
    contrasenia = hash_password(data.get('contrasenia'))

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "INSERT INTO usuarios (email, nombre, apellido, fechanac, contrasenia) VALUES (%s, %s, %s, %s, %s)"
    val = (email, nombre, apellido, fechanac, contrasenia)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario creado correctamente'}), 201
    except mysql.connector.Error as err:
        print(f"Error inserting usuario: {err}")
        return jsonify({'error': 'Error al crear el usuario'}), 500
    finally:
        if conn:
            conn.close()

# Endpoint to get all usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    data = {
        "rta":"ok",
        "usuarios": usuarios
    }

    return jsonify(data), 200



# Endpoint to check accesibility
@app.route('/check/<string:ip>', methods=['GET'])
def check_ip(ip):
    pingCmd = "ping -c 1 " + ip
    proc = subprocess.Popen(pingCmd, stdout=subprocess.PIPE, shell=True)
    # Obtener la salida estándar del proceso
    salida, error = proc.communicate()
    # Codificar la salida a un formato legible (por ejemplo, UTF-8)
    salida = salida.decode('utf-8')
    return jsonify(salida), 200
    


# Endpoint to get a usuario by email
@app.route('/usuarios/<string:email>', methods=['GET'])
def get_usuario(email):
    conn = connect_to_db()
    cursor = conn.cursor()
    print(email)

    # sql = "SELECT * FROM usuarios WHERE email = %s"
    sql = "SELECT * FROM usuarios WHERE email = " + email 
    val = (email,)
    # cursor.execute(sql, val)
    cursor.execute(sql)
    usuario = cursor.fetchone()

    data = {
        "rta":"ok",
    }

    if usuario:
        data["usuarios"] = usuario
        return jsonify(data), 200
    else:
        data["error"] = "usuario no encontrado"
        return jsonify(data), 404

# Endpoint to update a usuario
@app.route('/usuarios/<string:email>', methods=['PUT'])
def update_usuario(email):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fechanac = data.get('fechanac')

    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "UPDATE usuarios SET nombre = %s, apellido = %s, fechaNac = %s WHERE email = %s"
    val = (nombre, apellido, fechanac, email)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario actualizado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error updating usuario: {err}")
        return jsonify({'error': 'Error al actualizar el usuario'}), 500
    finally:
        if conn:
            conn.close()

# Endpoint to delete a usuario
@app.route('/usuarios/<string:email>', methods=['DELETE'])
def delete_usuario(email):
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = "DELETE FROM usuarios WHERE email = %s"
    val = (email,)

    try:
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
    except mysql.connector.Error as err:
        print(f"Error deleting usuario: {err}")
        return jsonify({'error': 'Error al eliminar el usuario'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(debug=True,host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0', port=443, ssl_context=('server.crt', 'server.key'))
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))

