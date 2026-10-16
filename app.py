from flask import Flask, render_template, jsonify, request
from registro import (cargar_datos, agregar_registro, editar_registro,
                      eliminar_registro)
from analisis import resumir
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "datos", "empresa.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dashboard")
def dashboard():
    registros = cargar_datos(DATA_FILE)
    return jsonify(resumir(registros))

def _json_body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}

def _error(msg, code):
    return jsonify({"error": msg}), code

@app.route("/api/registros", methods=["POST"])
def crear():
    try:
        return jsonify(agregar_registro(DATA_FILE, _json_body())), 201
    except ValueError as e:
        return _error(str(e), 400)

@app.route("/api/registros/<int:idx>", methods=["PUT"])
def actualizar(idx):
    try:
        return jsonify(editar_registro(DATA_FILE, idx, _json_body()))
    except LookupError as e:
        return _error(str(e), 404)
    except ValueError as e:
        return _error(str(e), 400)

@app.route("/api/registros/<int:idx>", methods=["DELETE"])
def borrar(idx):
    try:
        eliminar_registro(DATA_FILE, idx)
        return jsonify({"ok": True})
    except LookupError as e:
        return _error(str(e), 404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)