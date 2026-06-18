from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from lexer import analizar_lexico
from parser import validar_sintaxis
from interpreter import interpretar
from transformador import transformar
from afd import AFD_PRODUCTO

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")

def index():

    return render_template(
        "index.html"
    )

@app.route(
        
    "/procesar_excel",
    methods=["POST"]
)
def procesar_excel():    
    try:
        archivo = request.files["archivo"]
        ruta = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
        archivo.save(ruta)

        df = pd.read_excel(ruta)
        resultados = []

        # Asegúrate de que el nombre de la columna en Excel coincida
        # Si tu columna se llama "comando", esto funcionará:
        for index, row in df.iterrows():
            linea = str(row['comando']) 
            
            # 1. Validar
            validacion = validar_sintaxis(linea)
            
            if validacion["valido"]:
                # 2. Interpretar
                op_interpretada = interpretar(linea)
                # 3. Transformar
                resultado_final = transformar(op_interpretada)
                resultados.append({"fila": index + 1, "estado": "OK", "data": resultado_final})
            else:
                # Si falló la validación, guardamos el error
                resultados.append({"fila": index + 1, "estado": "Error", "detalles": validacion})

        return jsonify({
            "ok": True,
            "resultados": resultados
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        })
    
if __name__ == "__main__":

    app.run(
        debug=True
    )

@app.route("/afd")
def mostrar_afd():

    return render_template(
        "afd.html",
        tabla=AFD_PRODUCTO
    )




