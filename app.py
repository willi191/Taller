from flask import Flask, render_template, jsonify, request, redirect, url_for
from registro import cargar_datos
from analisis import resumir
import os
import csv

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "datos", "empresa.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dashboard")
def dashboard():
    try:
        registros = cargar_datos(DATA_FILE)
        return jsonify(resumir(registros))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/agregar", methods=["POST"])
def agregar():
    try:
        periodo = request.form.get("periodo")
        ventas = request.form.get("ventas")
        gastos = request.form.get("gastos")
        clientes = request.form.get("clientes")
        
        # Calcula la ganancia automáticamente restando ventas menos gastos
        ganancia = float(ventas) - float(gastos)
        
        # Guarda el nuevo registro respetando el formato CSV y el salto de línea
        with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([periodo, ventas, gastos, ganancia, clientes])
            
        return redirect(url_for("index"))
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)