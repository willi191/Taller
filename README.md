# Dashboard Empresarial Inteligente

Aplicación académica con Flask, CSV, análisis de indicadores y visualización con Chart.js.

## Requisitos
- Python 3.10 o superior
- Conexión a internet para cargar Chart.js desde CDN

## Instalación y ejecución
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python registro.py
python app.py
```
Abre http://127.0.0.1:5000 en el navegador. En una segunda terminal ejecuta `python registro.py` cuando quieras añadir registros. Pulsa “Actualizar datos” en el dashboard después de registrar información.

## Datos
Los datos se guardan en `datos/empresa.csv`. Usa valores no negativos para ventas, gastos y clientes. Los cálculos son descriptivos y las recomendaciones están basadas en reglas transparentes; no son asesoría financiera ni una predicción garantizada.

## Publicación
Para obtener una URL pública, despliega el proyecto en un servicio compatible con aplicaciones Python/Flask y configura el comando de inicio como `gunicorn app:app` (añadiendo `gunicorn` a requirements.txt). La captura de URL pública debe añadirse al documento una vez que el despliegue se haya completado y probado. El registro por consola está pensado para uso local; para producción multiusuario, debe sustituirse por un formulario web autenticado y una base de datos persistente.
