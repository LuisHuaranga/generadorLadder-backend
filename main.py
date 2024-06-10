from flask import Flask, jsonify, request
from flask_cors import CORS
from openAI import openaiConect as apenAI
import copy
import cProfile
import pstats
import io
from memory_profiler import memory_usage
import time

app = Flask(__name__)
CORS(app)
    
with open('prompts/prompt_test.txt', 'r') as file:
    prePrompt = file.read()

@app.route('/sendPrompt', methods=['POST'])
def sendPrompt():
    response = {}

    # Medir el uso de memoria inicial
    memoria_inicio = memory_usage(max_usage=True)
    # Iniciar el cronómetro
    inicio = time.perf_counter()
    # Crear un objeto de perfil y empezar a perfilarse
    pr = cProfile.Profile()
    pr.enable()

    try:
        body = request.json
        #logica para objeter el json de conecciones de PLC
        #response debe ser lo que retorna la funcion de openai
        response = copy.deepcopy(body)
        response['respuestaGTP'] = apenAI.generate_ladder_logic(prePrompt + body['prompt'])
        response['childVariableChange'] = 1
        httpRequest = 200

    except Exception as e:
        response['msgError'] = str(e)
        response['status'] = 0
        print(response)
        httpRequest = 500

    # Detener el perfilador de CPU
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    # Extraer solo la cantidad de llamadas y el tiempo de ejecución total
    profile_info = s.getvalue().split('\n')[0]

    # Detener el cronómetro
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    response['responseTimeSeg'] = tiempo_transcurrido

    # Medir el uso de memoria final y calcular la diferencia
    memoria_fin = memory_usage(max_usage=True)
    uso_memoria = memoria_fin - memoria_inicio
    response['memoryUsageMB'] = uso_memoria if uso_memoria >= 0 else 0  # Asegurar que el valor no sea negativo

    # Añadir la información del perfil de CPU al response
    response['cpuProfileSummary'] = profile_info

    return jsonify(response), httpRequest

def runApi():
    app.run(debug=True, port=8080)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
