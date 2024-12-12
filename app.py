from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from waitress import serve
import logging

# Configuración
from config import (
    ID_CLIENTE,
    AUTHORIZATION,
    BASE_URL,
    BASE_DE_DATOS_EMPLEADOS,
    BASE_DE_DATOS_VENDEDORES
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir solicitudes desde cualquier origen

# Configurar el nivel de logging
logging.basicConfig(level=logging.DEBUG)  # Cambiado a DEBUG para más detalles de depuración

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
            logging.warning("GET /api/empleados sin 'id'")
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Cliente/{empleado_id}"
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"GET request to URL: {url}")
        logging.debug(f"Headers: {headers}")

        response = requests.get(url, headers=headers)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"error": "Respuesta inválida del servidor externo"}), 500

    elif request.method == 'POST':
        data = request.json
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"POST request to URL: {url}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Data: {data}")

        response = requests.post(url, headers=headers, json=data)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"error": "Respuesta inválida del servidor externo"}), 500

    elif request.method == 'PUT':
        empleado_id = request.args.get('id')
        if not empleado_id:
            logging.warning("PUT /api/empleados sin 'id'")
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Cliente/{empleado_id}"
        data = request.json
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"PUT request to URL: {url}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Data: {data}")

        response = requests.put(url, headers=headers, json=data)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"error": "Respuesta inválida del servidor externo"}), 500

    elif request.method == 'DELETE':
        empleado_id = request.args.get('id')
        if not empleado_id:
            logging.warning("DELETE /api/empleados sin 'id'")
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Cliente/{empleado_id}/"
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = BASE_DE_DATOS_EMPLEADOS

        # Depuración: Registrar detalles de la solicitud
        logging.debug(f"DELETE request to URL: {url}")
        logging.debug(f"Headers: {headers}")

        response = requests.delete(url, headers=headers)

        # Depuración: Registrar detalles de la respuesta
        logging.debug(f"Response Status Code: {response.status_code}")
        logging.debug(f"Response Text: {response.text}")

        # Manejar la respuesta
        if response.status_code in [200, 204]:
            return jsonify({"message": "Empleado eliminado exitosamente"}), response.status_code
        else:
            try:
                data = response.json()
            except ValueError:
                data = {"error": response.text}
            return jsonify(data), response.status_code

@app.route('/api/vendedores', methods=['GET', 'POST', 'DELETE'])
def vendedores():
    url = f"{BASE_URL}/Vendedor/"
    # Obtener 'BaseDeDatos' de los parámetros de la solicitud, predeterminado a 'DEPOSEVN'
    base_de_datos = request.args.get('BaseDeDatos', BASE_DE_DATOS_VENDEDORES)
    headers = HEADERS.copy()
    headers["BaseDeDatos"] = base_de_datos

    if request.method == 'GET':
        vendedor_id = request.args.get('id')
        if not vendedor_id:
            logging.warning("GET /api/vendedores sin 'id'")
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Vendedor/{vendedor_id}"

        # Depuración
        logging.debug(f"GET request to URL: {url}")
        logging.debug(f"Headers: {headers}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Levanta excepción para códigos 4xx/5xx
            data = response.json()
            logging.debug(f"Response JSON: {data}")
            return jsonify(data), response.status_code
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - Response Text: {response.text}")
            return jsonify({"error": "Error en la solicitud HTTP"}), response.status_code
        except Exception as err:
            logging.error(f"Error inesperado: {err}")
            return jsonify({"error": "Error inesperado"}), 500

    elif request.method == 'POST':
        data = request.json
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = base_de_datos

        # Depuración
        logging.debug(f"POST request to URL: {url}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Data: {data}")

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            data = response.json()
            logging.debug(f"Response JSON: {data}")
            return jsonify(data), response.status_code
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - Response Text: {response.text}")
            return jsonify({"error": "Error en la solicitud HTTP"}), response.status_code
        except Exception as err:
            logging.error(f"Error inesperado: {err}")
            return jsonify({"error": "Error inesperado"}), 500

    elif request.method == 'DELETE':
        vendedor_id = request.args.get('id')
        if not vendedor_id:
            logging.warning("DELETE /api/vendedores sin 'id'")
            return jsonify({"error": "Falta el parámetro 'id'"}), 400
        url = f"{BASE_URL}/Vendedor/{vendedor_id}/"
        headers = HEADERS.copy()
        headers["BaseDeDatos"] = base_de_datos

        # Depuración
        logging.debug(f"DELETE request to URL: {url}")
        logging.debug(f"Headers: {headers}")

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            # Manejar la respuesta
            if response.status_code in [200, 204]:
                return jsonify({"message": "Vendedor eliminado exitosamente"}), response.status_code
            else:
                try:
                    data = response.json()
                except ValueError:
                    data = {"error": response.text}
                return jsonify(data), response.status_code
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} - Response Text: {response.text}")
            return jsonify({"error": "Error en la solicitud HTTP"}), response.status_code
        except Exception as err:
            logging.error(f"Error inesperado: {err}")
            return jsonify({"error": "Error inesperado"}), 500
