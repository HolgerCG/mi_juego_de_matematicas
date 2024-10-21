# interaccion.py

import os
import sys
import pygame
import speech_recognition as sr
import threading
import openai
import io
from pygame.locals import *
from compartido import mostrar_texto_centrado

# Usaremos pyttsx3 para la síntesis de voz con voz masculina
import pyttsx3
import re
import time

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Interacción con Asistente Matemático')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Fuentes
font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 32)  # Ajusta el tamaño si es necesario

# Configurar OpenAI
openai.api_key = 'sk-7Z1V2qIWwRWSYwOYvgAnBb71C3HDqWMwfrZPlaj6aaT3BlbkFJs3EMRbLTTM-I78D74RLibCykqPSi7tLpVi9QnGFRAA'  # Asegúrate de configurar la variable de entorno

# Inicializar pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Seleccionar una voz masculina (ajusta el índice según las voces disponibles)
for voice in voices:
    if "spanish" in voice.name.lower() and "male" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Función para obtener la ruta completa de un recurso
def obtener_ruta_recurso(ruta_relativa):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, ruta_relativa)

# Cargar sonidos
sonido_click = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/button_09-190435.mp3'))

# Variables globales
user_text = ''
response_text = ''
grabando = False
mostrando_habla_ahora = False
tiempo_inicio_grabacion = None
historial_mensajes = [
    {
        "role": "system",
        "content": (
            "Te llamas C.O.R.E.BOT, un asistente educativo diseñado por Holger Centeno bajo la dirección del PhD Orlando Erazo, para ayudar a niños de quinto año de educación básica en matemáticas. "
            "Tu objetivo es enseñar y explicar conceptos matemáticos de manera clara, sencilla y amigable. "
            "Si el niño hace una pregunta que no está relacionada con matemáticas de quinto grado, amablemente debes indicarle que solo puedes ayudar con ese tema y animarlo a seguir aprendiendo."
        )
    }
]

# Función para renderizar texto en múltiples líneas
def render_text_multiline(text, x, y, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        line_width, _ = font.size(test_line)
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    if current_line:
        lines.append(current_line)
    for i, line in enumerate(lines):
        line_surface = font.render(line.strip(), True, color)
        screen.blit(line_surface, (x, y + i * font.get_linesize()))

# Función para dividir el texto en oraciones sin NLTK
def dividir_en_oraciones(texto):
    # Utilizar expresiones regulares para dividir el texto en oraciones
    oraciones = re.split(r'(?<=[.!?]) +', texto)
    return oraciones

# Función principal de interacción
def interaccion():
    global grabando, user_text, response_text, mostrando_habla_ahora, historial_mensajes, tiempo_inicio_grabacion

    clock = pygame.time.Clock()

    # Fondo
    fondo_interaccion = pygame.image.load(obtener_ruta_recurso('imagenes/fondo_interactivo.jpg'))
    fondo_interaccion = pygame.transform.scale(fondo_interaccion, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Crear botón de "Volver al menú principal"
    boton_salir_rect = pygame.Rect(10, 10, 200, 50)  # Posición y tamaño del botón

    # Crear botones de "Iniciar" y "Detener" grabación
    boton_iniciar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, 120, 50)
    boton_detener_rect = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT - 80, 120, 50)

    while True:
        screen.blit(fondo_interaccion, (0, 0))

        # Dibujar botón de "Volver al menú principal"
        pygame.draw.rect(screen, RED, boton_salir_rect)
        texto_boton = font.render("Volver al menú", True, WHITE)
        texto_boton_rect = texto_boton.get_rect(center=boton_salir_rect.center)
        screen.blit(texto_boton, texto_boton_rect)

        # Dibujar botones de "Iniciar" y "Detener" grabación
        color_iniciar = GREEN if not grabando else DARK_GRAY
        color_detener = RED if grabando else DARK_GRAY

        pygame.draw.rect(screen, color_iniciar, boton_iniciar_rect)
        texto_iniciar = font.render("Iniciar", True, WHITE)
        texto_iniciar_rect = texto_iniciar.get_rect(center=boton_iniciar_rect.center)
        screen.blit(texto_iniciar, texto_iniciar_rect)

        pygame.draw.rect(screen, color_detener, boton_detener_rect)
        texto_detener = font.render("Detener", True, WHITE)
        texto_detener_rect = texto_detener.get_rect(center=boton_detener_rect.center)
        screen.blit(texto_detener, texto_detener_rect)

        # Mostrar texto del usuario y respuesta
        x_text = 50
        max_width = SCREEN_WIDTH - x_text - 50  # Margen derecho

        # Mostrar texto del usuario
        render_text_multiline(f"Tú: {user_text}", x_text, 150, font_large, BLACK, max_width)

        # Mostrar texto del asistente
        render_text_multiline(f"C.O.R.E.BOT: {response_text}", x_text, 220, font_large, BLACK, max_width)

        # Mostrar mensaje "Habla ahora" si es necesario
        if mostrando_habla_ahora:
            # Verificar si ha pasado el tiempo para ocultar el mensaje
            tiempo_transcurrido = time.time() - tiempo_inicio_grabacion
            if tiempo_transcurrido <= 1:  # Mostrar el mensaje solo por 1 segundo
                habla_surface = font_large.render("¡Habla ahora!", True, GREEN)
                habla_rect = habla_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(habla_surface, habla_rect)
            else:
                mostrando_habla_ahora = False  # Ocultar el mensaje después de 1 segundo

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if boton_iniciar_rect.collidepoint(event.pos) and not grabando:
                    sonido_click.play()
                    grabando = True
                    mostrando_habla_ahora = True
                    tiempo_inicio_grabacion = time.time()  # Registrar el tiempo de inicio
                    threading.Thread(target=grabar_audio).start()
                elif boton_detener_rect.collidepoint(event.pos) and grabando:
                    sonido_click.play()
                    grabando = False  # La función de grabación se encargará de detenerse
                elif boton_salir_rect.collidepoint(event.pos):
                    sonido_click.play()
                    return  # Volver al menú principal
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return  # Volver al menú principal

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

def grabar_audio():
    global user_text, response_text, grabando, historial_mensajes

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_list = []

        print("Grabando...")
        while grabando:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                audio_list.append(audio)
            except sr.WaitTimeoutError:
                continue

        if audio_list:
            # Unir todos los fragmentos de audio
            combined_audio = sr.AudioData(
                b''.join([a.get_raw_data() for a in audio_list]),
                audio_list[0].sample_rate,
                audio_list[0].sample_width
            )
            try:
                text = recognizer.recognize_google(combined_audio, language='es-ES')
                print(f"Tú dijiste: {text}")
                user_text = text

                # Añadir el mensaje del usuario al historial
                historial_mensajes.append({"role": "user", "content": text})

                # Obtener respuesta de la IA
                response_text = obtener_respuesta_ia(historial_mensajes)

                # Añadir la respuesta de la IA al historial
                historial_mensajes.append({"role": "assistant", "content": response_text})

                reproducir_respuesta(response_text)
            except sr.UnknownValueError:
                response_text = "No te he entendido, ¿puedes repetirlo?"
                reproducir_respuesta(response_text)
            except Exception as e:
                print(f"Error al procesar el audio: {e}")
                response_text = f"Lo siento, hubo un error al procesar tu solicitud: {e}"
                reproducir_respuesta(response_text)
        else:
            response_text = "No se recibió ningún audio."
            reproducir_respuesta(response_text)

def obtener_respuesta_ia(historial_mensajes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=historial_mensajes,
            temperature=0.7,
            max_tokens=300,
            n=1,
            stop=None
        )
        respuesta = response.choices[0].message['content'].strip()
        print(f"C.O.R.E.BOT: {respuesta}")
        return respuesta
    except Exception as e:
        print(f"Error al obtener respuesta de la IA: {e}")
        return f"Lo siento, hubo un error al procesar tu solicitud: {e}"

# Función para reproducir respuesta en voz usando pyttsx3
def reproducir_respuesta(texto):
    try:
        # Dividir el texto en oraciones sin NLTK
        oraciones = dividir_en_oraciones(texto)
        for oracion in oraciones:
            engine.say(oracion)
        engine.runAndWait()
    except Exception as e:
        print(f"Error al reproducir respuesta: {e}")
