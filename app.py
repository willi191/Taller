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
    registros = cargar_datos(DATA_FILE)
    return jsonify(resumir(registros))

@app.route("/agregar", methods=["POST"])
def agregar():
    try:
        periodo = request.form.get("periodo")
        ventas = request.form.get("ventas")
        gastos = request.form.get("gastos")
        clientes = request.form.get("clientes")
        
        ganancia = float(ventas) - float(gastos)
        
        with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([periodo, ventas, gastos, ganancia, clientes])
            
        return redirect(url_for("index"))
    except Exception as e:
        return str(e), 500

@app.route("/eliminar/<int:index>", methods=["POST"])
def eliminar(index):
    try:
        # Leer todas las filas del CSV
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            
        if not reader:
            return redirect(url_for("index"))
            
        header = reader[0]
        rows = reader[1:]
        
        # Eliminar la fila según el índice (index 0 en la tabla corresponde a rows[0])
        if 0 <= index < len(rows):
            rows.pop(index)
            
        # Reescribir el archivo completo de forma limpia
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
            
        return redirect(url_for("index"))
    except Exception as e:
        return str(e), 500

@app.route("/editar/<int:index>", methods=["POST"])
def editar(index):
    try:
        periodo = request.form.get("periodo")
        ventas = request.form.get("ventas")
        gastos = request.form.get("gastos")
        clientes = request.form.get("clientes")
        
        ganancia = float(ventas) - float(gastos)
        
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            
        if not reader:
            return redirect(url_for("index"))
            
        header = reader[0]
        rows = reader[1:]
        
        if 0 <= index < len(rows):
            rows[index] = [periodo, ventas, gastos, ganancia, clientes]
            
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
            
        return redirect(url_for("index"))
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)