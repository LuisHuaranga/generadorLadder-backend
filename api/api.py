from flask import Flask, jsonify, request
from flask_cors import CORS
import copy

import time #intentar borrar

app = Flask(__name__)
CORS(app)

@app.route('/sendPrompt',methods=['POST'])
def sendPrompt():
    inicio = time.perf_counter()
    try:
        body = request.json
        #logica para objeter el json de conecciones de PLC
        #response debe ser lo que retorna la funcion de openai
        time.sleep(3)
        response = copy.deepcopy(body)
        response['status'] = 1
        httpRequest = 200        
    
    except Exception as e:
        response['msgError'] = str(e)
        response['status'] = 0
        print(response)
        httpRequest = 500

    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    response['responseTimeSeg'] = tiempo_transcurrido
    return jsonify(response),httpRequest

if __name__ == '__main__':
    app.run(debug=True, port=8080)