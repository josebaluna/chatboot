import json
import random
from voice_utils import speak, listen, configure_input_output
from intent_utils import load_data, save_data, add_pattern_response, find_intent_by_tag, get_random_response, delete_responses, delete_intent, list_intents, show_help
from colorama import Fore

def main():
    data = load_data()

    print(Fore.CYAN + "Bot: ¿Quieres ingresar por voz o texto? (voz/texto)" + Fore.RESET)
    speak("¿Quieres ingresar por voz o texto?")
    input_mode, output_mode = configure_input_output()

    while True:
        if input_mode == "voz":
            user_input = listen().lower()
        else:
            user_input = input("Tú: ").strip().lower()

        if user_input in ['salir', 'exit']:
            if output_mode == "voz":
                speak("¡Hasta luego!")
            print(Fore.GREEN + "Bot: ¡Hasta luego!" + Fore.RESET)
            break

        if user_input == "cambiar_entrada":
            input_mode, output_mode = configure_input_output()
            continue

        if user_input == "cambiar_salida":
            input_mode, output_mode = configure_input_output(is_output=True)
            continue

        if user_input == "ayuda":
            help_text = show_help()
            if output_mode == "voz":
                speak(help_text)
            print(Fore.YELLOW + "Bot: " + help_text + Fore.RESET)
            continue

        # Comandos de añadir, ver, eliminar, etc.
        handle_commands(user_input, data, input_mode, output_mode)

def handle_commands(user_input, data, input_mode, output_mode):
    if user_input.startswith("añadir "):
        try:
            _, rest = user_input.split(' ', 1)
            tag, rest = rest.split(' ', 1)
            pattern, response = rest.split(':', 1)
            add_pattern_response(tag.strip(), pattern.strip(), response.strip(), data)
            save_data(data)
            response_text = f"Nuevo patrón y respuesta añadidos al intent '{tag}'."
            speak_or_print(response_text, output_mode)
        except ValueError:
            error_message = "Uso incorrecto. Usa: añadir <etiqueta> <patrón>: <respuesta>"
            speak_or_print(error_message, output_mode)
        return

    if user_input.startswith("ver "):
        tag = user_input[4:].strip()
        intent = find_intent_by_tag(tag, data)
        if intent:
            response_text = f"Patrones y respuestas para '{tag}':"
            speak_or_print(response_text, output_mode)
            for pattern in intent['patterns']:
                print(Fore.MAGENTA + f"- {pattern}" + Fore.RESET)
            for response in intent['responses']:
                print(Fore.MAGENTA + f"- {response}" + Fore.RESET)
        else:
            error_message = f"No se encontraron datos para la etiqueta '{tag}'."
            speak_or_print(error_message, output_mode)
        return

    if user_input.startswith("eliminar "):
        tag = user_input[9:].strip()
        intent = find_intent_by_tag(tag, data)
        if intent:
            print(f"Respuestas almacenadas para '{tag}':")
            for i, response in enumerate(intent['responses'], 1):
                print(Fore.MAGENTA + f"{i}. {response}" + Fore.RESET)
            indices_str = input("Ingresa los números de las respuestas a eliminar, separados por comas: ")
            try:
                indices = [int(index.strip()) - 1 for index in indices_str.split(",")]
                delete_responses(tag, indices, data)
                save_data(data)
                speak_or_print("Respuestas eliminadas correctamente.", output_mode)
            except ValueError:
                speak_or_print("Error al interpretar los índices. Asegúrate de ingresar números separados por comas.", output_mode)
        else:
            speak_or_print(f"No se encontraron datos para la etiqueta '{tag}'.", output_mode)
        return

    if user_input.startswith("eliminar_intent "):
        tag = user_input[16:].strip()
        if tag:
            delete_intent(tag, data)
            save_data(data)
            speak_or_print(f"La etiqueta '{tag}' y todas sus respuestas han sido eliminadas.", output_mode)
        else:
            speak_or_print("Debes proporcionar una etiqueta después de 'eliminar_intent'.", output_mode)
        return

    if user_input == "etiquetas":
        tags = list_intents(data)
        if tags:
            speak_or_print("Etiquetas almacenadas:", output_mode)
            for tag in tags:
                print(Fore.MAGENTA + f"- {tag}" + Fore.RESET)
        else:
            speak_or_print("No hay etiquetas almacenadas.", output_mode)
        return

    response = get_random_response(user_input, data)
    if response:
        speak_or_print(response, output_mode)
    else:
        response_text = "No sé la respuesta a eso. ¿Quieres darme una respuesta? ¿Y en qué etiqueta debo almacenarla?"
        speak_or_print(response_text, output_mode)
        new_response = input("Tu respuesta (o 'no' para omitir): ").strip()
        if new_response.lower() != 'no':
            print("Bot: ¿En qué etiqueta deseas almacenar esta respuesta?")
            tag = input("Etiqueta: ").strip()
            add_pattern_response(tag, user_input, new_response, data)
            save_data(data)
            speak_or_print("Gracias por la información. Ahora lo sé.", output_mode)

def speak_or_print(text, output_mode):
    if output_mode == "voz":
        speak(text)
    print(Fore.YELLOW + f"Bot: {text}" + Fore.RESET)

if __name__ == '__main__':
    main()
