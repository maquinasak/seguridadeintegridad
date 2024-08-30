from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/data')
def data():
    db_config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', 'my-secret-pw'),
        'database': os.getenv('MYSQL_DB', 'mydatabase'),
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM my_table")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
