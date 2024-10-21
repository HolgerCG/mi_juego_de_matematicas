import os
import pygame
import sys
from menu_niveles import mapa_niveles  # Asegúrate de que esta importación y función existan
from compartido import mostrar_texto_centrado # Importar funciones compartidas
from acerca_de import mostrar_acerca_de  # Importar mostrar_acerca_de desde acercade.py
from interaccion import interaccion  # Importar interaccion desde interaccion.py

# Función para obtener la ruta completa de un recurso
def obtener_ruta_recurso(ruta_relativa):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, ruta_relativa)

# Inicializar Pygame
pygame.init()

# Configuración de pantalla completa para Raspberry Pi (800x480) sin bordes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)  # Sin bordes
pygame.display.toggle_fullscreen()  # Pantalla completa

pygame.display.set_caption('Menú Principal - Juego Educativo')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# Cargar imagen de fondo
fondo_menu = pygame.image.load(obtener_ruta_recurso('imagenes/fondo_menu2.jpg'))
fondo_menu = pygame.transform.scale(fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar sonidos y música
pygame.mixer.music.load(obtener_ruta_recurso('sonidos/chiptune-grooving-142242.mp3'))  # Música de fondo
sonido_click = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/button_09-190435.mp3'))  # Sonido de clic en botones

# Configurar volumen
pygame.mixer.music.set_volume(0.5)
sonido_click.set_volume(0.5)

# Reproducir música de fondo en bucle
pygame.mixer.music.play(-1)

# Definir fuentes
font = pygame.font.Font(None, 50)
small_font = pygame.font.SysFont("Comic Sans MS", 24)  # Define small_font aquí

# Cargar íconos de sonido
icono_sonido_on = pygame.image.load(obtener_ruta_recurso('imagenes/sonido_on.png'))
icono_sonido_off = pygame.image.load(obtener_ruta_recurso('imagenes/sonido_off.png'))
icono_sonido_on = pygame.transform.scale(icono_sonido_on, (50, 50))
icono_sonido_off = pygame.transform.scale(icono_sonido_off, (50, 50))

# Estado del sonido
sonido_activado = True  # Inicialmente, el sonido está activado

# Función para dibujar botones "Siguiente", "Salir" y "Voz"
def dibujar_botones(screen):
    # Botón "Siguiente"
    boton_siguiente_rect = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 80, 160, 50)
    pygame.draw.rect(screen, BLACK, boton_siguiente_rect, border_radius=12)
    mostrar_texto_centrado('Siguiente', small_font, WHITE, boton_siguiente_rect, screen)

    # Botón "Salir"
    boton_salir_rect = pygame.Rect(20, SCREEN_HEIGHT - 80, 160, 50)
    pygame.draw.rect(screen, BLACK, boton_salir_rect, border_radius=12)
    mostrar_texto_centrado('Salir', small_font, WHITE, boton_salir_rect, screen)

    # Botón "Voz"
    boton_voz_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 50)
    pygame.draw.rect(screen, BLACK, boton_voz_rect, border_radius=12)
    mostrar_texto_centrado('Voz', small_font, WHITE, boton_voz_rect, screen)

# Función para mostrar el menú principal
def menu_principal():
    global sonido_activado  # Necesario para cambiar el estado del sonido

    while True:
        # Dibujar el fondo del menú principal con la imagen de fondo
        screen.blit(fondo_menu, (0, 0))

        # Definir botones del menú principal
        boton_juego = pygame.Rect(250, 120, 300, 70)
        boton_opcion2 = pygame.Rect(250, 220, 300, 70)
        boton_acerca = pygame.Rect(250, 320, 300, 70)
        boton_sonido_rect = pygame.Rect(700, 20, 50, 50)  # Botón de sonido

        # Dibujar los botones con contornos y color negro
        pygame.draw.rect(screen, BLACK, boton_juego, border_radius=10)
        pygame.draw.rect(screen, BLACK, boton_opcion2, border_radius=10)
        pygame.draw.rect(screen, BLACK, boton_acerca, border_radius=10)

        # Mostrar texto en cada botón con fondo negro y texto blanco
        mostrar_texto_centrado('Iniciar Juego', font, WHITE, boton_juego, screen)
        mostrar_texto_centrado('Interacción', font, WHITE, boton_opcion2, screen)
        mostrar_texto_centrado('Acerca de', font, WHITE, boton_acerca, screen)

        # Dibujar el icono de sonido según el estado actual
        if sonido_activado:
            screen.blit(icono_sonido_on, (boton_sonido_rect.x, boton_sonido_rect.y))  # Mostrar icono de sonido activado
        else:
            screen.blit(icono_sonido_off, (boton_sonido_rect.x, boton_sonido_rect.y))  # Mostrar icono de sonido desactivado

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_juego.collidepoint(event.pos):
                    sonido_click.play()  # Reproducir sonido al hacer clic en el botón
                    try:
                        mapa_niveles()  # Llamar a la función `mapa_niveles` cuando se presione el botón Iniciar Juego
                    except NameError:
                        print("Error: La función `mapa_niveles` no está definida.")
                elif boton_opcion2.collidepoint(event.pos):
                    sonido_click.play()  # Reproducir sonido al hacer clic en el botón
                    print("Interacción activada.")  # Acción para el botón Interacción (modificar según sea necesario)
                    interaccion()  # Llamar a la función `interaccion` cuando se presione el botón Interacción                
                elif boton_acerca.collidepoint(event.pos):
                    sonido_click.play()  # Reproducir sonido al hacer clic en el botón
                    mostrar_acerca_de(screen)  # Llamar a la función `mostrar_acerca_de` cuando se presione el botón Acerca de
                elif boton_sonido_rect.collidepoint(event.pos):  # Verificar colisión con el rectángulo de sonido
                    # Alternar el estado del sonido
                    sonido_activado = not sonido_activado
                    if sonido_activado:
                        pygame.mixer.music.set_volume(0.5)  # Activar sonido
                    else:
                        pygame.mixer.music.set_volume(0)  # Desactivar sonido

        pygame.display.update()

# Ejecutar el menú principal
menu_principal()
