from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from waitress import serve
import logging

# Configuración
from config import ID_CLIENTE, AUTHORIZATION, BASE_URL, BASE_DE_DATOS_EMPLEADOS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir solicitudes desde cualquier origen

# Configurar el nivel de logging
logging.basicConfig(level=logging.INFO)

HEADERS = {
    "accept": "application/json",
    "IdCliente": ID_CLIENTE,
    "Authorization": AUTHORIZATION,
    "Content-Type": "application/json"
}

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
    
    
@app.route('/api/vendedores', methods=['GET', 'POST', 'DELETE'])
def vendedores():
    url = f"{BASE_URL}/Vendedor/"
    params = {}
    data = {}

    # Obtener 'BaseDeDatos' de los parámetros de la solicitud, predeterminado a 'DEPOFORT'
    base_de_datos = request.args.get('BaseDeDatos', 'DEPOFORT')

    if request.method == 'GET':
        vendedor_id = request.args.get('id')
        if not vendedor_id:
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Vendedor/{vendedor_id}"
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = base_de_datos

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"GET request to URL: {url}")
        logging.debug(f"Headers: {headers}")

        response = requests.get(url, headers=headers)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        return jsonify(response.json()), response.status_code

    elif request.method == 'POST':
        data = request.json
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = base_de_datos

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"POST request to URL: {url}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Data: {data}")

        response = requests.post(url, headers=headers, json=data)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        return jsonify(response.json()), response.status_code

    elif request.method == 'DELETE':
        vendedor_id = request.args.get('id')
        if not vendedor_id:
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Vendedor/{vendedor_id}/"
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = base_de_datos

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"DELETE request to URL: {url}")
        logging.debug(f"Headers: {headers}")

        response = requests.delete(url, headers=headers)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        # Manejar la respuesta
        if response.status_code == 200 or response.status_code == 204:
            return jsonify({"message": "Vendedor eliminado exitosamente"}), response.status_code
        else:
            try:
                data = response.json()
            except ValueError:
                data = {"error": response.text}
            return jsonify(data), response.status_code  

# No es necesario el if __name__ == '__main__': para Render
