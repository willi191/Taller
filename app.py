from flask import Flask, render_template, jsonify
from registro import cargar_datos
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)