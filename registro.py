import csv, os
from datetime import datetime

CAMPOS = ["mes", "ventas", "gastos", "clientes"]

def registrar_por_consola(ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    existe = os.path.exists(ruta)
    print("\n=== REGISTRO DE DATOS EMPRESARIALES ===")
    print("Escribe 'fin' como mes para terminar.\n")
    with open(ruta, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        if not existe or os.path.getsize(ruta) == 0:
            writer.writeheader()
        while True:
            mes = input("Mes o periodo (ej. Enero 2026): ").strip()
            if mes.lower() == "fin":
                break
            if not mes:
                print("El periodo no puede estar vacío.")
                continue
            try:
                ventas = float(input("Ventas (COP): ").replace(",", "").strip())
                gastos = float(input("Gastos (COP): ").replace(",", "").strip())
                clientes = int(input("Número de clientes: ").strip())
                if ventas < 0 or gastos < 0 or clientes < 0:
                    raise ValueError
            except ValueError:
                print("Datos inválidos. Usa números no negativos. Intenta de nuevo.")
                continue
            writer.writerow({"mes": mes, "ventas": ventas, "gastos": gastos, "clientes": clientes})
            print("Registro guardado.\n")

def cargar_datos(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

if __name__ == "__main__":
    ruta = os.path.join(os.path.dirname(__file__), "datos", "empresa.csv")
    registrar_por_consola(ruta)
