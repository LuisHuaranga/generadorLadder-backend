import openai
import xml.etree.ElementTree as ET

# Configura tu clave API de OpenAI
openai.api_key = ''

def generar_respuesta(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def generar_salida_xml(pedido, respuesta):
    root = ET.Element("RespuestaAutomatizacion")
    pedido_element = ET.SubElement(root, "Pedido")
    pedido_element.text = pedido
    respuesta_element = ET.SubElement(root, "Respuesta")
    respuesta_element.text = respuesta

    return ET.tostring(root, encoding='utf-8').decode('utf-8')

def evaluar_expresion_booleana(expresion):
    try:
        # Evalúa la expresión booleana en un entorno seguro
        resultado = eval(expresion, {"__builtins__": None}, {})
        return resultado
    except Exception as e:
        return f"Error en la evaluación de la expresión booleana: {e}"

def main():
    # Solicitar al usuario el pedido de programación
    pedido = input("Introduce el pedido de programación para automatización industrial: ")

    # Generar la respuesta usando la API de OpenAI
    respuesta = generar_respuesta(pedido)
    print("\nRespuesta Generada:\n", respuesta)

    # Generar salida en XML
    salida_xml = generar_salida_xml(pedido, respuesta)
    print("\nSalida XML:\n", salida_xml)

    # Evaluar una expresión booleana de ejemplo
    expresion_booleana = "True and not False"
    resultado_booleana = evaluar_expresion_booleana(expresion_booleana)
    print("\nResultado de la expresión booleana '{}':\n{}".format(expresion_booleana, resultado_booleana))

if __name__ == "__main__":
    main()