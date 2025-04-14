import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty('rate', 120)  # Velocidad del habla
engine.setProperty('volume', 0.8)  # Volumen

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
        return ""
    except sr.RequestError:
        print("Error de solicitud; verifica tu conexión a Internet.")
        return ""

def configure_input_output(is_output=False):
    mode = input("Modo de entrada: ") if not is_output else input("Modo de salida: ")
    while mode not in ['voz', 'texto']:
        print("Opción inválida. Por favor, elige entre 'voz' o 'texto'.")
        mode = input("Modo de entrada: ") if not is_output else input("Modo de salida: ")
    return mode, mode
