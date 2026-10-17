"""
Estimador de pedidos de kits de robótica (CASO 01)
Flask + HTML + CSS (sin JavaScript).

Instalar:  pip install -r requirements.txt
Ejecutar:  python app.py   ->   abrir http://127.0.0.1:5000
"""
import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)


# ===========================================================================
# 1. MODELO Y CONFIGURACIÓN
# ===========================================================================
# modelo.json guarda los coeficientes de la regresión lineal (generado al entrenar):
# pedidos = intercepto + c1*consultas_web + c2*inversion_publicidad_soles + c3*campana_escolar
MODELO = json.loads(Path(__file__).with_name("modelo.json").read_text(encoding="utf-8"))

# Nombre de cada campo del formulario (se usa en los mensajes de error)
CAMPOS = {
    "consultas_web": "Consultas web",
    "inversion_publicidad_soles": "Inversión en publicidad (S/)",
    "campana_escolar": "Campaña escolar",
}


# ===========================================================================
# 2. LÓGICA: VALIDAR Y PREDECIR
# ===========================================================================
def validar(form):
    """Convierte los datos a número y revisa los rangos. Devuelve (valores, errores)."""
    valores, errores = {}, []
    for campo, etiqueta in CAMPOS.items():
        bruto = (form.get(campo) or "").strip().replace(",", ".")
        minimo, maximo = MODELO["rangos"][campo]
        try:
            numero = float(bruto)
        except ValueError:
            errores.append(f"{etiqueta}: escribe un número válido.")
            continue
        if numero != numero or numero in (float("inf"), float("-inf")):  # NaN / infinito
            errores.append(f"{etiqueta}: valor no permitido.")
        elif not (minimo <= numero <= maximo):
            errores.append(f"{etiqueta}: debe estar entre {minimo} y {maximo}.")
        elif campo == "campana_escolar" and numero not in (0, 1):
            errores.append(f"{etiqueta}: debe ser 0 (no) o 1 (sí).")
        else:
            valores[campo] = numero
    return valores, errores


def predecir(valores):
    """y = intercepto + suma(coeficiente * valor). Nunca devuelve negativos."""
    y = MODELO["intercepto"] + sum(
        MODELO["coeficientes"][c] * valores[c] for c in MODELO["columnas"]
    )
    return max(0.0, y)


# ===========================================================================
# 3. RUTA PRINCIPAL
# ===========================================================================
@app.route("/", methods=["GET", "POST"])
def index():
    valores, errores, resultado = {}, [], None
    if request.method == "POST":
        valores, errores = validar(request.form)
        if not errores:
            y = predecir(valores)
            mae = MODELO["metricas_prueba"]["mae"]
            resultado = {
                "pedidos": round(y),
                "exacto": round(y, 1),
                "minimo": max(0, round(y - mae)),
                "maximo": round(y + mae),
            }
        valores = {c: request.form.get(c, "") for c in CAMPOS}  # recordar lo escrito
    return render_template(
        "index.html", valores=valores, errores=errores, resultado=resultado,
        rangos=MODELO["rangos"], metricas=MODELO["metricas_prueba"],
    )


# ===========================================================================
# 4. ARRANQUE
# ===========================================================================
if __name__ == "__main__":
    app.run(debug=False)
