# 🤖 Asistente Interactivo por Voz y Texto

Este proyecto es un bot conversacional en Python que permite interactuar tanto por **voz** como por **texto**. Utiliza reconocimiento de voz para la entrada y síntesis de voz para la salida, además de almacenar patrones y respuestas en un archivo `training.json`.

---

## 🛠 Funcionalidades

- Reconocimiento de voz usando `speech_recognition`.
- Síntesis de voz con `pyttsx3`.
- Entrada/salida configurables: voz o texto.
- Sistema de intents con patrones y respuestas.
- Persistencia de datos en formato JSON.
- Comandos para:
  - Añadir nuevas frases y respuestas.
  - Ver intents existentes.
  - Eliminar respuestas o intents.
  - Listar etiquetas (tags).
  - Cambiar modos de entrada y salida.
  - Mostrar ayuda.

---

## ▶️ Requisitos

```bash
pip install pyttsx3 speechrecognition


## 🚀 Uso
bash
Copiar
Editar
python bot.py
Durante la ejecución, el bot te preguntará si querés usar voz o texto para interactuar, y si querés que las respuestas sean habladas o escritas.

## 🗂 Estructura de Datos
El archivo training.json contiene una lista de intents con esta estructura:

json
Copiar
Editar
{
  "intents": [
    {
      "tag": "saludo",
      "patterns": ["hola", "buen día"],
      "responses": ["¡Hola! ¿Cómo estás?", "Buen día, ¿en qué te puedo ayudar?"]
    }
  ]
}

## 💬 Comandos Disponibles
añadir <etiqueta> <patrón>: <respuesta>

ver <etiqueta>

eliminar <etiqueta> (respuestas)

eliminar_intent <etiqueta> (intento completo)

etiquetas

cambiar_entrada

cambiar_salida

ayuda

salir / exit

## 📌 Ejemplo
text
Copiar
Editar
Tú: añadir saludo Hola: ¡Hola! ¿Qué tal?
Tú: ver saludo
Tú: eliminar saludo
Tú: etiquetas
