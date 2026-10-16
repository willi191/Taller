import csv, os, tempfile, threading
from datetime import datetime

_lock = threading.Lock()

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

def _fmt(n):
    """Escribe enteros sin decimales (15000000 en vez de 15000000.0)."""
    return int(n) if float(n) == int(n) else n

def validar_registro(d):
    """Valida y normaliza un registro. Lanza ValueError con un mensaje claro."""
    mes = str(d.get("mes", "")).strip()
    if not mes:
        raise ValueError("El periodo no puede estar vacío.")
    if len(mes) > 60:
        raise ValueError("El periodo es demasiado largo (máx. 60 caracteres).")
    try:
        ventas = float(str(d.get("ventas", "")).replace(",", "").strip())
        gastos = float(str(d.get("gastos", "")).replace(",", "").strip())
        clientes = float(str(d.get("clientes", "")).strip())
    except ValueError:
        raise ValueError("Ventas, gastos y clientes deben ser números.")
    if min(ventas, gastos, clientes) < 0:
        raise ValueError("Ventas, gastos y clientes no pueden ser negativos.")
    if clientes != int(clientes):
        raise ValueError("El número de clientes debe ser un entero.")
    if ventas != ventas or gastos != gastos or ventas in (float("inf"),) or gastos in (float("inf"),):
        raise ValueError("Valores numéricos inválidos.")
    return {"mes": mes, "ventas": _fmt(ventas), "gastos": _fmt(gastos), "clientes": int(clientes)}

def guardar_datos(ruta, registros):
    """Reescribe el CSV completo de forma atómica (archivo temporal + reemplazo)."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(ruta), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS, extrasaction="ignore")
            writer.writeheader()
            for r in registros:
                writer.writerow({c: r.get(c, "") for c in CAMPOS})
        os.replace(tmp, ruta)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise

def _mes_duplicado(registros, mes, ignorar=None):
    m = mes.strip().lower()
    return any(i != ignorar and str(r.get("mes", "")).strip().lower() == m
               for i, r in enumerate(registros))

def agregar_registro(ruta, d):
    nuevo = validar_registro(d)
    with _lock:
        registros = cargar_datos(ruta)
        if _mes_duplicado(registros, nuevo["mes"]):
            raise ValueError(f"Ya existe un registro para «{nuevo['mes']}». Edítalo en lugar de crear otro.")
        registros.append(nuevo)
        guardar_datos(ruta, registros)
    return nuevo

def editar_registro(ruta, idx, d):
    nuevo = validar_registro(d)
    with _lock:
        registros = cargar_datos(ruta)
        if not 0 <= idx < len(registros):
            raise LookupError("El registro no existe (¿ya fue eliminado?). Actualiza los datos.")
        if _mes_duplicado(registros, nuevo["mes"], ignorar=idx):
            raise ValueError(f"Ya existe otro registro para «{nuevo['mes']}».")
        registros[idx] = nuevo
        guardar_datos(ruta, registros)
    return nuevo

def eliminar_registro(ruta, idx):
    with _lock:
        registros = cargar_datos(ruta)
        if not 0 <= idx < len(registros):
            raise LookupError("El registro no existe (¿ya fue eliminado?). Actualiza los datos.")
        eliminado = registros.pop(idx)
        guardar_datos(ruta, registros)
    return eliminado

if __name__ == "__main__":
    ruta = os.path.join(os.path.dirname(__file__), "datos", "empresa.csv")
    registrar_por_consola(ruta)