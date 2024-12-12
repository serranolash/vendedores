from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
from config import ID_CLIENTE, AUTHORIZATION, BASE_URL, BASE_DE_DATOS_EMPLEADOS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)

HEADERS = {
    "accept": "application/json",
    "IdCliente": ID_CLIENTE,
    "Authorization": AUTHORIZATION,
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return jsonify({"message": "Bienvenido a la API de Vendedores"})

@app.route('/api/empleados', methods=['GET', 'POST', 'PUT', 'DELETE'])
def empleados():
    url = f"{BASE_URL}/Cliente/"
    if request.method == 'GET':
        empleado_id = request.args.get('id')
        if not empleado_id:
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Cliente/{empleado_id}"
        response = requests.get(url, headers=HEADERS)
        return jsonify(response.json()), response.status_code

    elif request.method == 'POST':
        data = request.json
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS
        response = requests.post(url, headers=headers, json=data)
        return jsonify(response.json()), response.status_code

    elif request.method == 'PUT':
        empleado_id = request.args.get('id')
        if not empleado_id:
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Cliente/{empleado_id}"
        data = request.json
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS
        response = requests.put(url, headers=headers, json=data)
        return jsonify(response.json()), response.status_code

    elif request.method == 'DELETE':
        empleado_id = request.args.get('id')
        if not empleado_id:
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Cliente/{empleado_id}/"
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS
        response = requests.delete(url, headers=headers)
        return jsonify({"message": "Empleado eliminado exitosamente"}), response.status_code

# No es necesario el if __name__ == '__main__': para Render
