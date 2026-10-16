from flask import Flask, render_template, jsonify, request, redirect, url_for
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

# Ruta para agregar datos directamente desde el formulario web
@app.route("/agregar", methods=["POST"])
def agregar():
    try:
        periodo = request.form.get("periodo")
        ventas = request.form.get("ventas")
        gastos = request.form.get("gastos")
        clientes = request.form.get("clientes")
        
        # Calcula la ganancia automáticamente
        ganancia = float(ventas) - float(gastos)
        
        # Añade la nueva línea al archivo CSV manteniendo el formato
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{periodo},{ventas},{gastos},{ganancia},{clientes}")
            
        return redirect(url_for("index"))
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)