import openai
import json

# Configura tu clave API de OpenAI
openai.api_key = ''

def generate_ladder_logic(prompt):
    try:
        # Llama a la API de OpenAI para generar el código de PLC tipo ladder utilizando la nueva sintaxis
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        # Obtén el texto generado por GPT-3.5
        generated_text = response['choices'][0]['message']['content'].strip()

        # Devuelve la respuesta en formato JSON
        return json.dumps({"generated_ladder_logic": generated_text}, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

if __name__ == "__main__":
    prompt = input("Introduce el prompt para generar la programación de PLC tipo ladder: ")
    result = generate_ladder_logic(prompt)
    print(result)
