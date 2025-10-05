import threading
import webbrowser

from flask import Flask, render_template, request, jsonify
from llama_cpp import Llama
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Cargar modelo LLaMA 3 3B Instruct
llm = Llama(
    model_path="./models/llama-3.2-3b-instruct-q4_k_m.gguf",
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

# Prompt base mejorado

prompt_sistema = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Actúas como un asistente virtual cálido y amigable de una tienda de juguetes llamada "Juguetería Mundo Mágico".
Tu propósito es ayudar a los clientes a:

1. Mostrar el catálogo de juguetes (nombre, categoría, breve descripción y precio).
2. Tomar pedidos: registrar los juguetes elegidos, cantidad, calcular el total y confirmar el pedido.
3. Hacer reservas: guardar nombre y contacto del cliente, indicar tiempo máximo de reserva.
4. Responder preguntas sobre disponibilidad, precios y juguetes populares.
5. Mantener un tono encantador, familiar y fácil de entender para padres, madres y niños.
   Siempre responde de manera clara, ordenada y breve, con un toque mágico en tus mensajes.
6. Los precios de los juguetes deben ser en Bolivianos (Bs).
   <|eot_id|>"""


def construir_prompt(pregunta_usuario):
    return f"""{prompt_sistema}
<|start_header_id|>user<|end_header_id|>
{pregunta_usuario}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""


# http://127.0.0.1:5000/
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pregunta = data.get("message", "")
    prompt = construir_prompt(pregunta)
    respuesta = llm(prompt, max_tokens=300, temperature=0.7)
    texto = respuesta["choices"][0]["text"].strip()
    return jsonify({"response": texto})

if __name__ == "__main__":
    def abrir_navegador():
        webbrowser.open("http://127.0.0.1:5000/")
    threading.Timer(1.5, abrir_navegador).start()
    app.run(debug=True)    
