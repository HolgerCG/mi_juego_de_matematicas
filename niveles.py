import os
import pygame
import sys
import random
import speech_recognition as sr  # Importar speech_recognition para entrada de voz
from compartido import mostrar_texto_centrado  # Importamos la función compartida desde el archivo compartido.py

# Determina el directorio base del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Función para obtener la ruta completa de un recurso
def obtener_ruta_recurso(ruta_relativa):
    return os.path.join(BASE_DIR, ruta_relativa)

# Inicializar Pygame
pygame.init()

# Configuración de pantalla para Raspberry Pi (800x480)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Cargar fuentes
font = pygame.font.Font(obtener_ruta_recurso('fuentes/GamestationCond.otf'), 40)
small_font = pygame.font.Font(obtener_ruta_recurso('fuentes/GamestationCond.otf'), 20)
small_fontTabla = pygame.font.Font(obtener_ruta_recurso('fuentes/GamestationCond.otf'), 40)
smaller_font = pygame.font.Font(obtener_ruta_recurso('fuentes/GamestationCond.otf'), 18)

# Cargar imagen de fondo
fondo_menu = pygame.image.load(obtener_ruta_recurso('imagenes/Fondo_menu.png'))
fondo_menu = pygame.transform.scale(fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar imagen de fondo para las preguntas
fondo_pregunta = pygame.image.load(obtener_ruta_recurso('imagenes/fondo_preguntas.png'))
fondo_pregunta = pygame.transform.scale(fondo_pregunta, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Función para desbloquear el siguiente nivel (importada desde menu_niveles.py)
def desbloquear_nivel(nivel_actual):
    import menu_niveles
    menu_niveles.niveles_desbloqueados[nivel_actual] = True
    

# Generar una pregunta de multiplicación aleatoria basada en la tabla seleccionada
def generar_pregunta(tabla_seleccionada):
    num1 = tabla_seleccionada
    num2 = random.randint(1, 12)
    resultado_correcto = num1 * num2

    # Generar tres respuestas incorrectas que no sean iguales al resultado correcto
    respuestas_incorrectas = set()
    while len(respuestas_incorrectas) < 3:
        respuesta = random.randint(1, 144)
        if respuesta != resultado_correcto:
            respuestas_incorrectas.add(respuesta)

    respuestas = [resultado_correcto] + list(respuestas_incorrectas)
    random.shuffle(respuestas)
    
    return num1, num2, resultado_correcto, respuestas


# Menú para seleccionar la tabla de multiplicar (2 al 12)
def menu_tabla_multiplicar(screen, volver_al_mapa):
    while True:
        screen.blit(fondo_menu, (0, 0))

        # Definir posiciones exactas de los botones en la imagen
        botones = {
            'Tabla del 2': pygame.Rect(110, 180, 170, 60),
            'Tabla del 3': pygame.Rect(110, 240, 170, 60),
            'Tabla del 4': pygame.Rect(110, 300, 170, 60),
            'Tabla del 5': pygame.Rect(110, 360, 170, 60),
            'Tabla del 6': pygame.Rect(320, 180, 170, 60),
            'Tabla del 7': pygame.Rect(320, 240, 170, 60),
            'Tabla del 8': pygame.Rect(320, 300, 170, 60),
            'Tabla del 9': pygame.Rect(320, 360, 170, 60),
            'Tabla del 10': pygame.Rect(530, 180, 170, 60),
            'Tabla del 11': pygame.Rect(530, 240, 170, 60),
            'Tabla del 12': pygame.Rect(530, 300, 170, 60)
        }

        # Dibujar botón "ATRÁS" en la esquina superior izquierda
        boton_atras = pygame.Rect(10, 10, 100, 40)
        pygame.draw.rect(screen, BLACK, boton_atras)
        mostrar_texto_centrado('ATRÁS', smaller_font, WHITE, boton_atras, screen)

        # Mostrar el texto en los botones, alineado y centrado
        for tabla, rect in botones.items():
            mostrar_texto_centrado(tabla, smaller_font, WHITE, rect, screen)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Detectar si se presiona el botón "ATRÁS"
                if boton_atras.collidepoint(mouse_pos):
                    return volver_al_mapa()  # Regresar al mapa de niveles

                # Detectar selección de tabla
                for tabla, rect in botones.items():
                    if rect.collidepoint(mouse_pos):
                        tabla_seleccionada = int(tabla.split()[-1])  # Extraer el número de la tabla seleccionada
                        return tabla_seleccionada  # Salimos del menú y pasamos a las preguntas

        pygame.display.update()

# Función para mostrar una breve explicación al inicio de cada nivel
def mostrar_explicacion(screen, nivel):
    screen.fill(WHITE)
    if nivel == 1:
        texto = "Nivel 1: Practica las tablas de multiplicar seleccionadas."
    elif nivel == 2:
        texto = "Nivel 2: Resuelve multiplicaciones más avanzadas."
    elif nivel == 3:
        texto = "Nivel 3: ¡Batalla matemática! Responde para derrotar al enemigo."
    else:
        texto = "Bienvenido al juego de matemáticas."
    mostrar_texto_multilinea(texto, font, BLACK, pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200), screen)
    pygame.display.update()
    pygame.time.wait(4000)  # Mostrar la explicación por 5 segundos

# Función para manejar entrada de voz
def entrada_de_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {texto}")
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return ""
        except sr.RequestError as e:
            print(f"Error de reconocimiento de voz; {e}")
            return ""

# Función para mostrar un mensaje con fondo (Correcto o Incorrecto)
def mostrar_mensaje_con_fondo(screen, mensaje, fuente, color_texto, color_fondo, rect):
    # Dibujar el fondo (rectángulo)
    pygame.draw.rect(screen, color_fondo, rect)
    # Mostrar el mensaje centrado en el rectángulo
    mostrar_texto_centrado(mensaje, fuente, color_texto, rect, screen)

# Función de nivel con tabla seleccionada
def nivel(screen, volver_al_mapa, tabla_seleccionada):
    mostrar_explicacion(screen, 1)  # Mostrar explicación del nivel 1

    preguntas_restantes = 12
    aciertos = 0  # Contador de aciertos
    puntos = 0    # Contador de puntos (2 puntos por acierto)
    vidas = 7     # Vidas totales del juego (7 oportunidades en total)

    while preguntas_restantes > 0:
        # Mostrar el fondo de las preguntas
        screen.blit(fondo_pregunta, (0, 0))

        # Generar una pregunta aleatoria
        num1, num2, resultado_correcto, respuestas = generar_pregunta(tabla_seleccionada)

        # Mostrar la pregunta (centrada dentro del marco superior)
        mostrar_texto_centrado(f'{num1} x {num2} = ?', font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 6 - 30, 300, 100), screen)

        # Mostrar las respuestas dentro de los botones rojos
        mostrar_texto_centrado(str(respuestas[0]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50), screen)
        mostrar_texto_centrado(str(respuestas[1]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50), screen)
        mostrar_texto_centrado(str(respuestas[2]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50), screen)
        mostrar_texto_centrado(str(respuestas[3]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50), screen)

        # Mostrar los puntos en la esquina superior derecha
        mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH - 200, 10, 190, 40), screen)

        # Mostrar las vidas totales en la esquina superior izquierda
        mostrar_texto_centrado(f'Vidas: {vidas}', small_font, BLACK, pygame.Rect(10, 10, 190, 40), screen)

        # Dibujar los botones "Siguiente", "Salir" y "Voz"
        dibujar_botones(screen)

        respuesta_seleccionada = None
        resultado_mostrado = False

        while not resultado_mostrado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Limpiar la pantalla para quitar mensajes anteriores
                    screen.blit(fondo_pregunta, (0, 0))
                    mostrar_texto_centrado(f'{num1} x {num2} = ?', font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 6 - 30, 300, 100), screen)

                    # Volver a mostrar las respuestas y botones
                    mostrar_texto_centrado(str(respuestas[0]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50), screen)
                    mostrar_texto_centrado(str(respuestas[1]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50), screen)
                    mostrar_texto_centrado(str(respuestas[2]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50), screen)
                    mostrar_texto_centrado(str(respuestas[3]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50), screen)
                    
                    # Volver a mostrar los puntos y las vidas totales
                    mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH - 200, 10, 190, 40), screen)
                    mostrar_texto_centrado(f'Vidas: {vidas}', small_font, BLACK, pygame.Rect(10, 10, 190, 40), screen)

                    # Volver a dibujar botones
                    dibujar_botones(screen)

                    # Detectar la respuesta seleccionada según la posición del clic
                    if SCREEN_WIDTH // 3 - 50 <= mouse_pos[0] <= SCREEN_WIDTH // 3 + 50 and SCREEN_HEIGHT // 2 - 60 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 - 10:
                        respuesta_seleccionada = respuestas[0]
                    elif SCREEN_WIDTH * 2 // 3 - 50 <= mouse_pos[0] <= SCREEN_WIDTH * 2 // 3 + 50 and SCREEN_HEIGHT // 2 - 60 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 - 10:
                        respuesta_seleccionada = respuestas[1]
                    elif SCREEN_WIDTH // 3 - 50 <= mouse_pos[0] <= SCREEN_WIDTH // 3 + 50 and SCREEN_HEIGHT // 2 + 40 - 50 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 90:
                        respuesta_seleccionada = respuestas[2]
                    elif SCREEN_WIDTH * 2 // 3 - 50 <= mouse_pos[0] <= SCREEN_WIDTH * 2 // 3 + 50 and SCREEN_HEIGHT // 2 + 40 - 50 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 90:
                        respuesta_seleccionada = respuestas[3]

                    # Botón de entrada de voz
                    if SCREEN_WIDTH // 2 - 80 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 80 and SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 30:
                        respuesta_voz = entrada_de_voz()
                        if respuesta_voz.isdigit():
                            respuesta_seleccionada = int(respuesta_voz)
                        else:
                            mostrar_mensaje_con_fondo(screen, 'No se entendió la respuesta.', smaller_font, WHITE, RED, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            continue

                    if respuesta_seleccionada is not None:
                        # Comprobar si la respuesta es correcta o incorrecta
                        if respuesta_seleccionada == resultado_correcto:
                            aciertos += 1  # Sumar un acierto
                            puntos += 2    # Sumar 2 puntos por acierto
                            mostrar_mensaje_con_fondo(screen, '¡Correcto!', font, WHITE, GREEN, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()

                            # Esperar 1 segundo y pasar a la siguiente pregunta automáticamente
                            pygame.time.wait(1000)
                            resultado_mostrado = True  # Salir del bucle para ir a la siguiente pregunta
                        else:
                            vidas -= 1  # Quitar una vida por intento fallido
                            mostrar_mensaje_con_fondo(screen, '¡Incorrecto! Inténtalo de nuevo.', smaller_font, WHITE, RED, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()

                            # Esperar 1 segundo para mostrar el mensaje de incorrecto y luego limpiarlo
                            pygame.time.wait(1000)

                            # Limpiar la pantalla nuevamente (solo si la respuesta es incorrecta)
                            screen.blit(fondo_pregunta, (0, 0))
                            mostrar_texto_centrado(f'{num1} x {num2} = ?', font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 6 - 30, 300, 100), screen)

                            # Volver a mostrar las respuestas, puntos y vidas
                            mostrar_texto_centrado(str(respuestas[0]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50), screen)
                            mostrar_texto_centrado(str(respuestas[1]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50), screen)
                            mostrar_texto_centrado(str(respuestas[2]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50), screen)
                            mostrar_texto_centrado(str(respuestas[3]), small_fontTabla, BLACK, pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50), screen)
                            mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH - 200, 10, 190, 40), screen)
                            mostrar_texto_centrado(f'Vidas: {vidas}', small_font, BLACK, pygame.Rect(10, 10, 190, 40), screen)

                            dibujar_botones(screen)

                            # Si el jugador pierde todas las vidas, finalizar el juego
                            if vidas == 0:
                                game_over(screen, puntos, volver_al_mapa)
                                return  # Finalizar el juego

                    # Comprobar si se hace clic en el botón "Siguiente" (solo disponible en caso de error)
                    if SCREEN_WIDTH - 180 <= mouse_pos[0] <= SCREEN_WIDTH - 20 and SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 30:
                        resultado_mostrado = True  # Salir del bucle cuando se presiona "Siguiente"

                    # Comprobar si se hace clic en el botón "Salir"
                    if 20 <= mouse_pos[0] <= 180 and SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 30:
                        return  # Regresar al menú de selección de tablas

            pygame.display.update()

        preguntas_restantes -= 1

    # Mostrar el puntaje final y mensaje de victoria
    screen.fill(WHITE)
    mostrar_texto_centrado('¡Felicidades! Has ganado', font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 50), screen)
    mostrar_texto_centrado(f'Aciertos: {aciertos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 50), screen)
    mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50), screen)
    pygame.display.update()
    sonido_victoria.play()  # Reproducir sonido de victoria
    pygame.time.wait(5000)  # Esperar 5 segundos para mostrar el puntaje

    volver_al_mapa()

# Función para mostrar pantalla de "Game Over" cuando el jugador pierde
def game_over(screen, puntos, volver_al_mapa):
    screen.fill(WHITE)
    mostrar_texto_centrado('¡Has perdido!, No te desanimes sigue practicando', font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 50), screen)
    mostrar_texto_centrado(f'Total Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50), screen)
    mostrar_texto_centrado('Inténtalo de nuevo', small_font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 50), screen)
    pygame.display.update()
    
    # Esperar 5 segundos antes de volver al mapa de tablas
    pygame.time.wait(5000)
    volver_al_mapa()  # Redirigir al menú de selección de 
    


#---------------------------------------------------2do NIVEL----------------------------------------------

# Generar una pregunta aleatoria para el segundo nivel con respuestas correctas
def generar_pregunta_segundo_nivel():
    tipo_pregunta = random.choice(["multiplicacion_dos_digitos", "combinacion_operaciones", "resultado_faltante"])
    
    if tipo_pregunta == "multiplicacion_dos_digitos":
        # Multiplicación con dos dígitos
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        resultado_correcto = num1 * num2
        
        # Generar respuestas incorrectas distintas y únicas
        respuestas_incorrectas = set()
        while len(respuestas_incorrectas) < 3:
            incorrecta = random.randint(100, 9999)
            if incorrecta != resultado_correcto:
                respuestas_incorrectas.add(incorrecta)
        
        # Añadir la respuesta correcta y mezclar
        respuestas = [resultado_correcto] + list(respuestas_incorrectas)
        random.shuffle(respuestas)
        pregunta = f"{num1} x {num2} = ?"
        return pregunta, resultado_correcto, respuestas

    elif tipo_pregunta == "combinacion_operaciones":
        # Combinación de operaciones: multiplicación + suma o resta
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        num3 = random.randint(1, 10)
        operacion = random.choice(["+", "-"])
        
        if operacion == "+":
            resultado_correcto = num1 * num2 + num3
            pregunta = f"{num1} x {num2} + {num3} = ?"
        else:
            resultado_correcto = num1 * num2 - num3
            pregunta = f"{num1} x {num2} - {num3} = ?"
        
        respuestas_incorrectas = set()
        while len(respuestas_incorrectas) < 3:
            incorrecta = random.randint(10, 100)
            if incorrecta != resultado_correcto:
                respuestas_incorrectas.add(incorrecta)
        
        respuestas = [resultado_correcto] + list(respuestas_incorrectas)
        random.shuffle(respuestas)
        return pregunta, resultado_correcto, respuestas

    elif tipo_pregunta == "resultado_faltante":
        # Multiplicación con número faltante
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
        resultado_correcto = num1 * num2
        posicion_faltante = random.choice([1, 2])  # Falta el primer número o el segundo

        if posicion_faltante == 1:
            pregunta = f"? x {num2} = {resultado_correcto}"
            respuestas = [num1, random.randint(1, 12), random.randint(1, 12), random.randint(1, 12)]
        else:
            pregunta = f"{num1} x ? = {resultado_correcto}"
            respuestas = [num2, random.randint(1, 12), random.randint(1, 12), random.randint(1, 12)]

        random.shuffle(respuestas)
        return pregunta, num1 if posicion_faltante == 1 else num2, respuestas

# Función del segundo nivel
def nivel_2(screen, volver_al_mapa):
    mostrar_explicacion(screen, 2)  # Mostrar explicación del nivel 2

    preguntas_restantes = 12
    aciertos = 0  # Contador de aciertos
    puntos = 0    # Contador de puntos (2 puntos por acierto)
    vidas = 7     # Vidas totales del juego (7 oportunidades en total)
    mensaje_mostrado = False  # Para manejar el tiempo de visualización de mensajes

    # Colores para los mensajes
    COLOR_CORRECTO = (0, 255, 0)
    COLOR_INCORRECTO = (255, 0, 0)

    while preguntas_restantes > 0 and vidas > 0:
        # Generar una pregunta aleatoria del segundo nivel
        pregunta, resultado_correcto, respuestas = generar_pregunta_segundo_nivel()

        # Rectángulos para la presentación de respuestas
        rect_pregunta = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 6 - 30, 300, 100)
        rect_respuestas = [
            pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50),
            pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 - 60, 100, 50),
            pygame.Rect(SCREEN_WIDTH // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50),
            pygame.Rect(SCREEN_WIDTH * 2 // 3 - 50, SCREEN_HEIGHT // 2 + 40, 100, 50)
        ]

        # Mostrar la pregunta inicial y las respuestas
        screen.blit(fondo_pregunta, (0, 0))  # Fondo inicial
        mostrar_texto_centrado(pregunta, font, BLACK, rect_pregunta, screen)
        for idx, rect in enumerate(rect_respuestas):
            mostrar_texto_centrado(str(respuestas[idx]), small_fontTabla, BLACK, rect, screen)
        mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH - 200, 10, 190, 40), screen)
        mostrar_texto_centrado(f'Vidas: {vidas}', small_font, BLACK, pygame.Rect(10, 10, 190, 40), screen)
        dibujar_botones(screen)
        pygame.display.update()  # Actualizar la pantalla inicial

        respuesta_seleccionada = None
        resultado_mostrado = False
        ha_respondido = False  # Para evitar penalizar antes de seleccionar una respuesta
        tiempo_inicio_mensaje = None
        mostrar_correcto = False  # Bandera para mostrar el mensaje "¡Correcto!"

        while not resultado_mostrado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Detectar la respuesta seleccionada
                    for idx, rect in enumerate(rect_respuestas):
                        if rect.collidepoint(mouse_pos):
                            respuesta_seleccionada = respuestas[idx]
                            ha_respondido = True

                    # Detectar botón "Siguiente"
                    if SCREEN_WIDTH - 180 <= mouse_pos[0] <= SCREEN_WIDTH - 20 and SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 30:
                        if not ha_respondido:
                            vidas -= 1  # Penalizar por no responder antes de pasar
                            mensaje_mostrado = True
                            tiempo_inicio_mensaje = pygame.time.get_ticks()
                            mostrar_mensaje_con_fondo(screen, '¡Incorrecto! No respondiste.', smaller_font, WHITE, COLOR_INCORRECTO, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()
                        resultado_mostrado = True

                    # Detectar botón "Salir"
                    if 20 <= mouse_pos[0] <= 180 and SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 30:
                        return volver_al_mapa()  # Regresar al mapa de niveles

                    # Detectar botón de entrada de voz
                    if SCREEN_WIDTH // 2 - 80 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 80 and SCREEN_HEIGHT - 80 <= mouse_pos[1] <= SCREEN_HEIGHT - 30:
                        respuesta_voz = entrada_de_voz()
                        if respuesta_voz.isdigit():
                            respuesta_seleccionada = int(respuesta_voz)
                            ha_respondido = True
                        else:
                            mostrar_mensaje_con_fondo(screen, 'No se entendió la respuesta.', smaller_font, WHITE, RED, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            continue

                    # Verificar si la respuesta seleccionada es correcta
                    if respuesta_seleccionada is not None:
                        if respuesta_seleccionada == resultado_correcto:
                            aciertos += 1
                            puntos += 2
                            mensaje_mostrado = True
                            mostrar_correcto = True  # Bandera para mostrar "¡Correcto!"
                            tiempo_inicio_mensaje = pygame.time.get_ticks()
                            # Mostrar mensaje "¡Correcto!" en color verde y centrarlo
                            mostrar_mensaje_con_fondo(screen, '¡Correcto!', font, WHITE, COLOR_CORRECTO, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()
                            resultado_mostrado = True  # Salir del bucle para la siguiente pregunta
                        else:
                            vidas -= 1
                            mensaje_mostrado = True
                            mostrar_correcto = False  # Bandera para no mostrar "¡Correcto!"
                            tiempo_inicio_mensaje = pygame.time.get_ticks()
                            # Mostrar mensaje "¡Incorrecto!" en color rojo
                            mostrar_mensaje_con_fondo(screen, '¡Incorrecto! Inténtalo de nuevo.', smaller_font, WHITE, COLOR_INCORRECTO, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 50))
                            pygame.display.update()
                            respuesta_seleccionada = None  # Permitir reintento
                            ha_respondido = False

            # Mostrar mensajes por un breve período sin bloquear el flujo
            if mensaje_mostrado and tiempo_inicio_mensaje:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - tiempo_inicio_mensaje >= 1000:  # Mostrar por 1 segundo
                    mensaje_mostrado = False
                    tiempo_inicio_mensaje = None
                    # Limpiar mensaje y mostrar pregunta nuevamente
                    screen.blit(fondo_pregunta, (0, 0))
                    mostrar_texto_centrado(pregunta, font, BLACK, rect_pregunta, screen)
                    for idx, rect in enumerate(rect_respuestas):
                        mostrar_texto_centrado(str(respuestas[idx]), small_fontTabla, BLACK, rect, screen)
                    mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH - 200, 10, 190, 40), screen)
                    mostrar_texto_centrado(f'Vidas: {vidas}', small_font, BLACK, pygame.Rect(10, 10, 190, 40), screen)
                    dibujar_botones(screen)
                    pygame.display.update()  # Refrescar la pantalla con la nueva pregunta y opciones

        preguntas_restantes -= 1

    # Mostrar el puntaje final y mensaje de victoria
    screen.fill(WHITE)
    mostrar_texto_centrado('¡Felicidades! Has ganado', font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 50), screen)
    mostrar_texto_centrado(f'Aciertos: {aciertos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 50), screen)
    mostrar_texto_centrado(f'Puntos: {puntos}', small_font, BLACK, pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50), screen)
    pygame.display.update()
    sonido_victoria.play()  # Reproducir sonido de victoria
    pygame.time.wait(3000)  # Mostrar el puntaje por 3 segundos antes de volver al mapa

    volver_al_mapa()

# Dibujar botones "Siguiente", "Salir" y "Voz"
def dibujar_botones(screen):
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 160, 50))
    mostrar_texto_centrado('Siguiente', small_font, WHITE, pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 160, 50), screen)

    pygame.draw.rect(screen, BLACK, (20, SCREEN_HEIGHT - 80, 160, 50))
    mostrar_texto_centrado('Salir', small_font, WHITE, pygame.Rect(20, SCREEN_HEIGHT - 80, 160, 50), screen)

    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 50))
    mostrar_texto_centrado('Voz', small_font, WHITE, pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 50), screen)

# Nivel 1
def nivel_1(screen, volver_al_mapa):
    tabla_seleccionada = menu_tabla_multiplicar(screen, volver_al_mapa)
    if tabla_seleccionada:
        nivel(screen, volver_al_mapa, tabla_seleccionada)

#-------------- Nivel 3 -----------

# Definir colores
COLOR_JUGADOR = (0, 255, 0)  # Verde para la barra de vida del jugador
COLOR_ENEMIGO = (255, 0, 0)  # Rojo para la barra de vida del enemigo
COLOR_FONDO = (200, 200, 200)  # Fondo de pantalla para contraste
COLOR_TEXTO = (0, 0, 0)  # Negro para el texto
COLOR_BOTONES = (255, 255, 255)  # Blanco para los botones de respuesta

# Variables de vida
VIDA_JUGADOR = 100
VIDA_ENEMIGO = 100

# Cargar fuentes
font = pygame.font.Font(None, 60)  # Tamaño de fuente ajustado para el enunciado
small_font = pygame.font.Font(None, 50)  # Fuente ajustada para las respuestas
large_font = pygame.font.Font(None, 80)  # Fuente grande para el texto final
smaller_font = pygame.font.Font(None, 30)  # Fuente más pequeña para mensajes

# Cargar imágenes del jugador y del enemigo
imagen_jugador = pygame.image.load(obtener_ruta_recurso('imagenes/jugador.png'))
imagen_jugador = pygame.transform.scale(imagen_jugador, (100, 100))
imagen_enemigo = pygame.image.load(obtener_ruta_recurso('imagenes/enemigo.png'))
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (100, 100))

# Cargar imágenes de los proyectiles (espada y lanza)
imagen_espada = pygame.image.load(obtener_ruta_recurso('imagenes/espada.png')) # Imagen de la espada del jugador
imagen_espada = pygame.transform.scale(imagen_espada, (50, 10))  # Redimensionar para proyectil

imagen_lanza = pygame.image.load(obtener_ruta_recurso('imagenes/lanza.png')) # Imagen de la lanza del enemigo
imagen_lanza = pygame.transform.scale(imagen_lanza, (50, 10)) # Redimensionar para proyectil

# Cargar sonidos
sonido_correcto = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/correctoarco.mp3'))
sonido_incorrecto = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/enemigo_te_pega.mp3'))
sonido_victoria = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/GANASTE_MED.mp3'))
sonido_derrota = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/PERDISTE.mp3'))



# Funciones auxiliares del nivel 3
# Generar preguntas de razonamiento basadas en multiplicación para la batalla
def generar_pregunta_razonamiento_multiplicacion():
    # Listas de preguntas clasificadas
    preguntas_faciles = [
    ("Si compro 2 manzanas a $3 cada una, ¿cuánto gasto en total?", 6, [4, 5, 6, 7]),
    ("Si hay 5 días en una semana laboral, ¿cuántos días hay en 2 semanas laborales?", 10, [8, 10, 12, 14]),
    ("Tengo 3 cajas con 2 lápices cada una, ¿cuántos lápices tengo en total?", 6, [5, 6, 7, 8]),
    ("Si un gato tiene 4 patas, ¿cuántas patas tienen 2 gatos?", 8, [6, 7, 8, 9]),
    ("Ana tiene 5 flores y María tiene 3 flores, ¿cuántas flores tienen en total?", 8, [7, 8, 9, 10]),
    ("Si un carrito tiene 4 ruedas, ¿cuántas ruedas tienen 3 carritos?", 12, [10, 11, 12, 13]),
    ("Hay 2 pájaros en cada árbol y hay 5 árboles, ¿cuántos pájaros hay en total?", 10, [8, 9, 10, 11]),
    ("Si cada semana tengo 7 días, ¿cuántos días hay en 2 semanas?", 14, [12, 13, 14, 15]),
    ("Tengo 4 bolsas con 3 canicas cada una, ¿cuántas canicas tengo en total?", 12, [11, 12, 13, 14]),
    ("Si un pulpo tiene 8 tentáculos, ¿cuántos tentáculos tienen 2 pulpos?", 16, [14, 15, 16, 17]),
    ("Pedro tiene 3 paquetes de galletas con 5 galletas cada uno, ¿cuántas galletas tiene en total?", 15, [13, 14, 15, 16]),
    ("Si una bicicleta tiene 2 ruedas, ¿cuántas ruedas tienen 4 bicicletas?", 8, [6, 7, 8, 9]),
    ("Hay 5 dedos en una mano, ¿cuántos dedos hay en 3 manos?", 15, [14, 15, 16, 17]),
    ("Si cada auto tiene 4 puertas, ¿cuántas puertas hay en 2 autos?", 8, [7, 8, 9, 10]),
    ("Tengo 6 paquetes de stickers con 2 stickers cada uno, ¿cuántos stickers tengo?", 12, [10, 11, 12, 13]),
    ("Si en cada mesa hay 4 sillas y hay 3 mesas, ¿cuántas sillas hay en total?", 12, [11, 12, 13, 14]),
    ("Cada araña tiene 8 patas, ¿cuántas patas tienen 2 arañas?", 16, [15, 16, 17, 18]),
    ("Si una semana tiene 7 días, ¿cuántos días hay en 3 semanas?", 21, [20, 21, 22, 23]),
    ("En un coro hay 5 niños, si hay 4 coros, ¿cuántos niños hay en total?", 20, [18, 19, 20, 21]),
    ("Si cada paquete tiene 10 caramelos y compro 2 paquetes, ¿cuántos caramelos tengo?", 20, [18, 19, 20, 21]),
    ("Hay 2 ojos en una cara, ¿cuántos ojos hay en 6 caras?", 12, [11, 12, 13, 14]),
    ("Si cada día como 1 manzana, ¿cuántas manzanas como en 7 días?", 7, [6, 7, 8, 9]),
    ("Tengo 5 libros y cada libro tiene 2 marcadores, ¿cuántos marcadores tengo?", 10, [8, 9, 10, 11]),
    ("Si una hora tiene 60 minutos, ¿cuántos minutos hay en 2 horas?", 120, [110, 115, 120, 125]),
    ("En un jardín hay 3 filas de 4 flores, ¿cuántas flores hay en total?", 12, [10, 11, 12, 13]),
    ("Si cada niño tiene 2 globos y hay 5 niños, ¿cuántos globos hay en total?", 10, [9, 10, 11, 12]),
    ("Tengo 4 cajas y en cada una hay 3 pelotas, ¿cuántas pelotas tengo?", 12, [11, 12, 13, 14]),
    ("Si cada camiseta cuesta $5 y compro 3 camisetas, ¿cuánto pago?", 15, [12, 13, 14, 15]),
    ("Hay 6 huevos en una caja, ¿cuántos huevos hay en 2 cajas?", 12, [10, 11, 12, 13]),
    ("Si una docena son 12 unidades, ¿cuántas unidades hay en 1 docena?", 12, [11, 12, 13, 14]),
    ("En una jaula hay 2 conejos, ¿cuántas patas tienen en total?", 8, [6, 7, 8, 9])
    ]

    preguntas_intermedias = [
    ("Si un trabajador gana $15 por hora y trabaja 8 horas al día, ¿cuánto gana en un día?", 120, [110, 115, 120, 125]),
    ("En una granja hay 12 gallinas y cada una pone 5 huevos, ¿cuántos huevos hay en total?", 60, [50, 55, 60, 65]),
    ("Si un autobús puede llevar 40 pasajeros, ¿cuántos pasajeros pueden viajar en 3 autobuses?", 120, [110, 115, 120, 125]),
    ("Tengo 9 paquetes de 6 caramelos cada uno, ¿cuántos caramelos tengo en total?", 54, [50, 52, 54, 56]),
    ("Si cada caja contiene 25 lápices y tengo 4 cajas, ¿cuántos lápices tengo?", 100, [90, 95, 100, 105]),
    ("Un árbol frutal produce 30 manzanas al día, ¿cuántas manzanas produce en 5 días?", 150, [140, 145, 150, 155]),
    ("Si cada persona necesita 2 metros de tela y hay 20 personas, ¿cuánta tela se necesita?", 40, [38, 39, 40, 41]),
    ("En una biblioteca hay 8 estantes con 15 libros cada uno, ¿cuántos libros hay en total?", 120, [110, 115, 120, 125]),
    ("Si un coche consume 7 litros de gasolina cada 100 km, ¿cuántos litros necesita para 300 km?", 21, [18, 20, 21, 22]),
    ("Tengo 5 bolsas y en cada una hay 18 naranjas, ¿cuántas naranjas tengo en total?", 90, [85, 88, 90, 92]),
    ("Si una clase dura 45 minutos, ¿cuántos minutos hay en 6 clases?", 270, [260, 265, 270, 275]),
    ("En un torneo hay 16 equipos y cada equipo juega 3 partidos, ¿cuántos partidos se juegan en total?", 48, [45, 46, 48, 50]),
    ("Si un tren tiene 8 vagones y cada vagón puede llevar 50 pasajeros, ¿cuántos pasajeros en total?", 400, [380, 390, 400, 410]),
    ("Una fábrica produce 200 botellas al día, ¿cuántas botellas produce en una semana de 7 días?", 1400, [1350, 1380, 1400, 1420]),
    ("Si una máquina puede hacer 30 piezas por hora, ¿cuántas piezas hace en un turno de 8 horas?", 240, [230, 235, 240, 245]),
    ("Tengo 12 cajas con 12 chocolates cada una, ¿cuántos chocolates tengo en total?", 144, [140, 142, 144, 146]),
    ("Si un ciclista recorre 25 km al día, ¿cuántos kilómetros recorrerá en 5 días?", 125, [120, 123, 125, 128]),
    ("En un teatro hay 20 filas con 15 asientos cada una, ¿cuántos asientos hay en total?", 300, [290, 295, 300, 305]),
    ("Si un libro tiene 250 páginas y leo 10 páginas al día, ¿en cuántos días lo termino?", 25, [23, 24, 25, 26]),
    ("Una piscina se llena con 50 litros de agua por minuto, ¿cuántos litros en 30 minutos?", 1500, [1450, 1475, 1500, 1525]),
    ("Si una granja tiene 15 vacas y cada una da 8 litros de leche al día, ¿cuántos litros en total?", 120, [115, 118, 120, 123]),
    ("Un paquete de galletas cuesta $2 y compro 20 paquetes, ¿cuánto gasto en total?", 40, [35, 38, 40, 42]),
    ("Si hay 24 horas en un día, ¿cuántas horas hay en 3 días?", 72, [68, 70, 72, 74]),
    ("Tengo 7 camisas y cada una tiene 8 botones, ¿cuántos botones en total?", 56, [54, 55, 56, 57]),
    ("Si un aula tiene 5 filas de 6 pupitres, ¿cuántos pupitres hay en total?", 30, [28, 29, 30, 31]),
    ("En una feria hay 10 juegos y cada juego cuesta 3 tickets, ¿cuántos tickets necesito para jugar todos?", 30, [28, 29, 30, 31]),
    ("Si una botella contiene 1.5 litros y tengo 12 botellas, ¿cuántos litros tengo en total?", 18, [16, 17, 18, 19]),
    ("Un restaurante tiene 12 mesas y en cada mesa caben 4 personas, ¿cuántas personas en total?", 48, [45, 46, 48, 50]),
    ("Si un corredor da 4 vueltas en una pista de 400 metros, ¿cuántos metros corre en total?", 1600, [1500, 1550, 1600, 1650]),
    ("Tengo 9 cajas de huevos y cada caja tiene 12 huevos, ¿cuántos huevos tengo?", 108, [104, 106, 108, 110]),
    ("Si un mes tiene 30 días, ¿cuántos días hay en 6 meses?", 180, [175, 178, 180, 183])
    ]

    preguntas_dificiles = [
    ("Una fábrica produce 250 coches al día. ¿Cuántos coches producirá en 4 días?", 1000, [900, 950, 1000, 1050]),
    ("Si una caja contiene 24 latas y compro 7 cajas, ¿cuántas latas tengo en total?", 168, [160, 168, 176, 184]),
    ("Un avión vuela a 800 km/h. ¿Cuántos kilómetros recorrerá en 5 horas?", 4000, [3800, 4000, 4200, 4400]),
    ("Si un tren recorre 120 km en 2 horas, ¿cuántos kilómetros recorrerá en 7 horas?", 420, [400, 420, 440, 460]),
    ("Una empresa tiene 150 empleados y cada uno trabaja 8 horas al día. ¿Cuántas horas de trabajo en total al día?", 1200, [1100, 1150, 1200, 1250]),
    ("Si una máquina puede producir 500 piezas en una hora, ¿cuántas piezas en un turno de 9 horas?", 4500, [4300, 4400, 4500, 4600]),
    ("En un estadio caben 50,000 personas. Si se llenan 3 estadios, ¿cuántas personas hay en total?", 150000, [140000, 145000, 150000, 155000]),
    ("Una biblioteca tiene 20 estantes y cada estante contiene 500 libros. ¿Cuántos libros hay en total?", 10000, [9500, 10000, 10500, 11000]),
    ("Si un camión puede transportar 2000 kg y necesito mover 10,000 kg, ¿cuántos viajes necesito?", 5, [4, 5, 6, 7]),
    ("Un avión tiene 200 asientos y realiza 4 vuelos al día. ¿Cuántos pasajeros puede transportar en un día?", 800, [750, 800, 850, 900]),
    ("Si una cosechadora puede cosechar 150 hectáreas en un día, ¿cuántas hectáreas en 6 días?", 900, [850, 900, 950, 1000]),
    ("Una empresa fabrica 2,500 unidades de un producto por semana. ¿Cuántas unidades en 4 semanas?", 10000, [9500, 10000, 10500, 11000]),
    ("Si una computadora procesa 1,200 datos por minuto, ¿cuántos datos procesa en 2.5 horas?", 180000, [175000, 180000, 185000, 190000]),
    ("Un satélite orbita la Tierra 16 veces al día. ¿Cuántas órbitas en una semana?", 112, [108, 110, 112, 114]),
    ("Si una línea de montaje produce 60 coches por hora, ¿cuántos coches en un turno de 12 horas?", 720, [700, 710, 720, 730]),
    ("Un tanque tiene capacidad de 15,000 litros. Si se llena con una manguera que suministra 500 litros por minuto, ¿cuánto tarda en llenarse?", 30, [28, 29, 30, 31]),
    ("Si una población crece en 2,000 personas al año, ¿cuántas personas crecerá en 15 años?", 30000, [28000, 29000, 30000, 31000]),
    ("Un depósito de agua pierde 250 litros por hora debido a una fuga. ¿Cuántos litros pierde en un día?", 6000, [5800, 5900, 6000, 6100]),
    ("Si una fábrica trabaja 24 horas al día y produce 100 piezas por hora, ¿cuántas piezas produce en 5 días?", 12000, [11500, 11800, 12000, 12200]),
    ("Un astronauta viaja a una velocidad de 28,000 km/h. ¿Cuántos kilómetros recorre en 3 horas?", 84000, [82000, 83000, 84000, 85000]),
    ("Si una bomba de agua puede llenar 3,600 litros en una hora, ¿cuántos litros en 45 minutos?", 2700, [2600, 2650, 2700, 2750]),
    ("Una planta embotelladora produce 5,000 botellas por hora. ¿Cuántas botellas en un día de 24 horas?", 120000, [115000, 118000, 120000, 122000]),
    ("Si un corazón late 70 veces por minuto, ¿cuántas veces late en un día?", 100800, [100000, 100800, 101600, 102400]),
    ("Un generador produce 1.5 megavatios por hora. ¿Cuántos megavatios produce en un mes de 30 días?", 1080, [1000, 1040, 1080, 1120]),
    ("Si un avión recorre 900 km en 1.5 horas, ¿cuánto recorrerá en 8 horas?", 4800, [4600, 4700, 4800, 4900]),
    ("Un telescopio espacial toma 12 imágenes por hora. ¿Cuántas imágenes en una semana?", 2016, [2000, 2016, 2032, 2048]),
    ("Si una empresa tiene ingresos de $250,000 al mes, ¿cuáles son sus ingresos en un año?", 3000000, [2900000, 2950000, 3000000, 3050000]),
    ("Un atleta entrena 4 horas al día, quemando 600 calorías por hora. ¿Cuántas calorías quema en 5 días?", 12000, [11500, 11800, 12000, 12200]),
    ("Si la Tierra tarda 365 días en orbitar el Sol, ¿cuántos días en 12 órbitas?", 4380, [4320, 4350, 4380, 4410]),
    ("Un río fluye a 2,000 litros por segundo. ¿Cuántos litros fluyen en una hora?", 7200000, [7100000, 7150000, 7200000, 7250000]),
    ("Si un bibliotecario puede catalogar 30 libros por hora, ¿cuántos libros en una semana laboral de 40 horas?", 1200, [1150, 1180, 1200, 1220]),
    ]


    # Aumentar la dificultad según la vida del enemigo
    if VIDA_ENEMIGO > 60:
        pregunta, respuesta_correcta, opciones = random.choice(preguntas_faciles)
    elif VIDA_ENEMIGO > 30:
        pregunta, respuesta_correcta, opciones = random.choice(preguntas_intermedias)
    else:
        pregunta, respuesta_correcta, opciones = random.choice(preguntas_dificiles)
    
    random.shuffle(opciones)  # Aleatorizar las opciones
    return pregunta, respuesta_correcta, opciones

# Dibujar la barra de vida del jugador y del enemigo
def dibujar_barra_vida(screen, vida_jugador, vida_enemigo):
    # Barra de vida del jugador
    pygame.draw.rect(screen, COLOR_JUGADOR, (50, 50, vida_jugador * 2, 30))  # Escalar la vida a 200 píxeles
    mostrar_texto_centrado(f'Jugador: {vida_jugador}%', small_font, COLOR_TEXTO, pygame.Rect(50, 20, 200, 30), screen)

    # Barra de vida del enemigo
    pygame.draw.rect(screen, COLOR_ENEMIGO, (550, 50, vida_enemigo * 2, 30))  # Escalar la vida a 200 píxeles
    mostrar_texto_centrado(f'Enemigo: {vida_enemigo}%', small_font, COLOR_TEXTO, pygame.Rect(550, 20, 200, 30), screen)


# Dibujar botones "Siguiente", "Salir" y "Voz"
def dibujar_botones(screen):
    # Botón "Siguiente"
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 160, 50))
    mostrar_texto_centrado('Siguiente', small_font, WHITE, pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 160, 50), screen)

    # Botón "Salir"
    pygame.draw.rect(screen, BLACK, (20, SCREEN_HEIGHT - 80, 160, 50))
    mostrar_texto_centrado('Salir', small_font, WHITE, pygame.Rect(20, SCREEN_HEIGHT - 80, 160, 50), screen)

    # Botón "Voz"
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 50))
    mostrar_texto_centrado('Voz', small_font, WHITE, pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 50), screen)

# Animación del ataque del jugador y el enemigo
def animar_ataque(screen, proyectil, inicio_x, inicio_y, final_x, final_y, velocidad=10):
    x, y = inicio_x, inicio_y
    while (x < final_x and inicio_x < final_x) or (x > final_x and inicio_x > final_x):
        screen.blit(proyectil, (x, y))  # Dibujar el proyectil en la posición actual
        pygame.display.update()
        pygame.time.delay(50)  # Pausa para animación
        screen.fill(COLOR_FONDO, (x, y, proyectil.get_width(), proyectil.get_height()))  # Limpiar la posición anterior
        x += velocidad if inicio_x < final_x else -velocidad  # Mover en la dirección correcta

# Función para dividir y centrar el enunciado en varias líneas
def mostrar_texto_multilinea(texto, fuente, color, rect, screen):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        if fuente.size(linea_actual + " " + palabra)[0] < rect.width:
            linea_actual += " " + palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    
    lineas.append(linea_actual)
    
    for i, linea in enumerate(lineas):
        texto_surface = fuente.render(linea.strip(), True, color)
        texto_rect = texto_surface.get_rect(center=(rect.x + rect.width // 2, rect.y + (i + 1) * (rect.height // (len(lineas) + 1))))
        screen.blit(texto_surface, texto_rect)

        

# Función de nivel 3 - Batalla Matemática
def nivel_3(screen, volver_al_mapa):
    global VIDA_JUGADOR, VIDA_ENEMIGO  # Utilizar las variables globales
    VIDA_JUGADOR = 100
    VIDA_ENEMIGO = 100

    mostrar_explicacion(screen, 3)  # Mostrar explicación del nivel 3

    ronda_actual = 1
    max_rondas = 5

    # Fondo de pantalla para la batalla
    fondo_pregunta = pygame.image.load(r'imagenes/nivel3_modified (3).png')
    fondo_pregunta = pygame.transform.scale(fondo_pregunta, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while VIDA_JUGADOR > 0 and VIDA_ENEMIGO > 0 and ronda_actual <= max_rondas:
        # Mostrar fondo
        screen.blit(fondo_pregunta, (0, 0))

        # Dibujar barra de vida del jugador y del enemigo
        dibujar_barra_vida(screen, VIDA_JUGADOR, VIDA_ENEMIGO)

        # Mostrar imágenes del jugador y del enemigo en la parte inferior
        screen.blit(imagen_jugador, (50, SCREEN_HEIGHT - 150))  # Jugador en la parte inferior izquierda
        screen.blit(imagen_enemigo, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150))  # Enemigo en la parte inferior derecha

        # Generar pregunta y mostrarla
        pregunta, respuesta_correcta, respuestas = generar_pregunta_razonamiento_multiplicacion()
        # Mostrar la pregunta en varias líneas, posicionada más abajo para dejar espacio para la barra de vida
        mostrar_texto_multilinea(pregunta, font, COLOR_TEXTO, pygame.Rect(SCREEN_WIDTH // 2 - 350, 100, 700, 150), screen)

        # Aleatorizar posiciones de las respuestas
        posiciones_respuestas = [
            pygame.Rect(100, 250, 100, 50),
            pygame.Rect(250, 250, 100, 50),
            pygame.Rect(400, 250, 100, 50),
            pygame.Rect(550, 250, 100, 50)
        ]
        random.shuffle(posiciones_respuestas)  # Aleatorizar posiciones

        for idx, rect in enumerate(posiciones_respuestas):
            pygame.draw.rect(screen, COLOR_BOTONES, rect)  # Dibujar el fondo del botón
            mostrar_texto_centrado(str(respuestas[idx]), small_font, COLOR_TEXTO, rect, screen)

        pygame.display.update()  # Actualizar pantalla con las respuestas

        # Bucle de eventos para seleccionar una respuesta
        respuesta_seleccionada = None
        while respuesta_seleccionada is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for idx, rect in enumerate(posiciones_respuestas):
                        if rect.collidepoint(mouse_pos):
                            respuesta_seleccionada = respuestas[idx]

                # Botón de entrada de voz (opcional)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:  # Presionar 'v' para activar entrada de voz
                        respuesta_voz = entrada_de_voz()
                        if respuesta_voz.isdigit():
                            respuesta_seleccionada = int(respuesta_voz)
                        else:
                            mostrar_mensaje_con_fondo(screen, 'No se entendió la respuesta.', smaller_font, WHITE, RED, pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50, 400, 50))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            continue

            pygame.display.update()

        # Verificar si la respuesta es correcta
        if respuesta_seleccionada == respuesta_correcta:
            # El jugador ataca al enemigo con la espada
            animar_ataque(screen, imagen_espada, 150, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100)
            VIDA_ENEMIGO -= 20
            sonido_correcto.play()  # Reproducir sonido correcto
            mostrar_mensaje_con_fondo(screen, '¡Correcto! Atacaste al enemigo.', smaller_font, WHITE, GREEN, pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50, 400, 50))
        else:
            # El enemigo ataca al jugador con la lanza hacia la izquierda
            animar_ataque(screen, imagen_lanza, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 150, SCREEN_HEIGHT - 100)
            VIDA_JUGADOR -= 20
            sonido_incorrecto.play()  # Reproducir sonido incorrecto
            mostrar_mensaje_con_fondo(screen, '¡Incorrecto! El enemigo te atacó.', smaller_font, WHITE, RED, pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50, 400, 50))

        pygame.display.update()
        pygame.time.wait(1000)  # Pausa para mostrar el mensaje

        ronda_actual += 1  # Incrementar la ronda

    # Final de la batalla
    screen.fill(COLOR_FONDO)
    if VIDA_ENEMIGO <= 0:
        sonido_victoria.play()  # Reproducir sonido de victoria
        mostrar_texto_centrado('¡Felicidades! Has ganado', large_font, COLOR_TEXTO, pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50, 600, 100), screen)
    elif VIDA_JUGADOR <= 0:
        sonido_derrota.play()  # Reproducir sonido de derrota
        mostrar_texto_centrado('¡Batalla terminada!', large_font, COLOR_TEXTO, pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 150, 600, 100), screen)
        mostrar_texto_centrado('¡Perdiste la batalla! :C ', large_font, COLOR_TEXTO, pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50, 600, 100), screen)
        mostrar_texto_centrado('¡Sigue practicando!', large_font, COLOR_TEXTO, pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 50, 600, 100), screen)
    else:
        mostrar_texto_centrado('¡Batalla terminada!', large_font, COLOR_TEXTO, pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50, 600, 100), screen)

    pygame.display.update()
    pygame.time.wait(5000)  # Pausa antes de volver al mapa

    volver_al_mapa()  # Volver al mapa de niveles

# Mostrar texto centrado en un rectángulo
def mostrar_texto_centrado(texto, fuente, color, rect, screen):
    superficie = fuente.render(texto, True, color)
    texto_rect = superficie.get_rect()
    texto_rect.center = (rect.x + rect.width // 2, rect.y + rect.height // 2)
    screen.blit(superficie, texto_rect)
