import json
import os
import random

def load_data(filename='training.json'):
    if not os.path.isfile(filename):
        print(f"Archivo '{filename}' no encontrado. Creando un nuevo archivo.")
        return {"intents": []}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: El archivo JSON está corrupto. Creando un nuevo archivo.")
        return {"intents": []}

def save_data(data, filename='training.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError:
        print("Error: No se pudo guardar el archivo.")

def add_pattern_response(tag, pattern, response, data):
    intent = find_intent_by_tag(tag, data)
    if intent:
        if pattern not in intent['patterns']:
            intent['patterns'].append(pattern)
        if response not in intent['responses']:
            intent['responses'].append(response)
    else:
        data['intents'].append({"tag": tag, "patterns": [pattern], "responses": [response]})

def find_intent_by_tag(tag, data):
    for intent in data['intents']:
        if intent['tag'].lower() == tag.lower():
            return intent
    return None

def get_random_response(pattern, data):
    intent = find_intent_by_pattern(pattern, data)
    if intent and intent['responses']:
        return random.choice(intent['responses'])
    return None

def find_intent_by_pattern(pattern, data):
    for intent in data['intents']:
        if pattern.lower() in [p.lower() for p in intent['patterns']]:
            return intent
    return None

def delete_responses(tag, indices, data):
    intent = find_intent_by_tag(tag, data)
    if intent:
        intent['responses'] = [resp for i, resp in enumerate(intent['responses']) if i not in indices]

def delete_intent(tag, data):
    data['intents'] = [intent for intent in data['intents'] if intent['tag'].lower() != tag.lower()]

def list_intents(data):
    return sorted(intent['tag'] for intent in data['intents'])

def show_help():
    return """
Comandos disponibles:
1. Preguntar: Introduce un patrón y el bot intentará responder.
2. añadir <etiqueta> <patrón>: <respuesta>: Añade un nuevo patrón y respuesta a un intent existente o crea una nueva entrada.
3. ver <etiqueta>: Muestra todos los patrones y respuestas almacenados para una etiqueta específica.
4. eliminar <etiqueta>: Elimina una o varias respuestas de una etiqueta específica.
5. eliminar_intent <etiqueta>: Elimina una etiqueta completa y todas sus respuestas.
6. etiquetas: Muestra una lista de todas las etiquetas almacenadas, ordenadas alfabéticamente.
7. cambiar_entrada: Cambia el modo de entrada entre voz y texto.
8. cambiar_salida: Cambia el modo de salida entre voz y texto.
9. ayuda: Muestra esta lista de comandos y cómo utilizarlos.
10. salir / exit: Termina la conversación con el bot.
    """
