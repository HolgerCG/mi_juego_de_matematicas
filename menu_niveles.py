import os
import pygame
import sys
from niveles import nivel_1, nivel_2, nivel_3  # Importar los niveles

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Juego de Matemáticas - Mapa de Niveles')

# Cargar imagen de fondo del mapa
mapa_fondo = pygame.image.load(obtener_ruta_recurso('imagenes/mapa_juego.jpg'))
mapa_fondo = pygame.transform.scale(mapa_fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar sonidos y música
pygame.mixer.music.load(obtener_ruta_recurso('sonidos/chiptune-grooving-142242.mp3'))  # Música de fondo
sonido_click = pygame.mixer.Sound(obtener_ruta_recurso('sonidos/button_09-190435.mp3'))  # Sonido de clic en botones

# Configurar volumen
pygame.mixer.music.set_volume(0.5)
sonido_click.set_volume(0.5)

# Reproducir música de fondo en bucle
pygame.mixer.music.play(-1)

# Definir posiciones de los niveles en el mapa (x, y, radio del círculo ajustado)
niveles = {
    'Nivel 1': (150, 200, 40),  # Coordenadas (x, y) y radio del círculo más pequeño
    'Nivel 2': (400, 150, 40),
    'Nivel 3': (650, 300, 40)
}

# Estado de la música
musica_activada = True  # Música activada al inicio

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir fuentes
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 24)

# Cargar íconos de sonido
icono_sonido_on = pygame.image.load(obtener_ruta_recurso('imagenes/sonido_on.png'))
icono_sonido_off = pygame.image.load(obtener_ruta_recurso('imagenes/sonido_off.png'))
icono_sonido_on = pygame.transform.scale(icono_sonido_on, (50, 50))
icono_sonido_off = pygame.transform.scale(icono_sonido_off, (50, 50))

# Función para mostrar texto centrado en un rectángulo
def mostrar_texto_centrado(superficie, texto, x, y, ancho, alto, color):
    label = font.render(texto, True, color)
    rect = label.get_rect(center=(x + ancho // 2, y + alto // 2))
    superficie.blit(label, rect)

# Función para mostrar el número dentro de un círculo
def mostrar_numero(numero, fuente, color, x, y):
    superficie = fuente.render(numero, True, color)
    rect = superficie.get_rect()
    rect.center = (x, y)
    screen.blit(superficie, rect)

# Función para el mapa de selección de niveles
def mapa_niveles():
    global musica_activada  # Usar las variables globales para gestionar el estado

    while True:
        screen.blit(mapa_fondo, (0, 0))  # Dibujar fondo del mapa

        # Dibujar los círculos de los niveles y los números en ellos
        for i, (nivel, (x, y, radio)) in enumerate(niveles.items(), start=1):
            pygame.draw.circle(screen, (255, 0, 0), (x, y), radio)  # Dibujar círculos en color rojo
            mostrar_numero(str(i), font, (255, 255, 255), x, y)  # Números en blanco dentro de los círculos

        # Dibujar botones adicionales (Sonido y Menú Principal)
        boton_sonido = pygame.Rect(700, 20, 50, 50)
        boton_menu = pygame.Rect(20, 20, 150, 50)

        # Dibujar el icono de sonido según el estado actual
        if musica_activada:
            screen.blit(icono_sonido_on, (boton_sonido.x, boton_sonido.y))  # Mostrar icono de sonido activado
        else:
            screen.blit(icono_sonido_off, (boton_sonido.x, boton_sonido.y))  # Mostrar icono de sonido desactivado

        # Dibujar el botón "Menú Principal"
        pygame.draw.rect(screen, BLACK, boton_menu)
        mostrar_texto_centrado(screen, 'Volver', boton_menu.x, boton_menu.y, boton_menu.width, boton_menu.height, WHITE)

        # Manejar eventos de selección de nivel
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Comprobar si se hace clic en el botón de sonido
                if boton_sonido.collidepoint(mouse_pos):
                    musica_activada = not musica_activada
                    if musica_activada:
                        pygame.mixer.music.unpause()  # Reanudar música solo si estaba en pausa
                    else:
                        pygame.mixer.music.pause()  # Pausar música

                # Comprobar si se hace clic en el botón "Menú Principal"
                elif boton_menu.collidepoint(mouse_pos):
                    sonido_click.play()  # Reproducir sonido de clic
                    return  # Regresar al menú principal (suponiendo que esta función es llamada desde allí)

                # Comprobar selección de niveles (todos los niveles están siempre disponibles)
                for i, (nivel, (x, y, radio)) in enumerate(niveles.items(), start=1):
                    if (x - radio) <= mouse_pos[0] <= (x + radio) and (y - radio) <= mouse_pos[1] <= (y + radio):
                        sonido_click.play()  # Reproducir sonido al seleccionar un nivel
                        # Dependiendo del nivel seleccionado, cargar el nivel correspondiente
                        if i == 1:
                            nivel_1(screen, mapa_niveles)  # Inicia Nivel 1
                        elif i == 2:
                            nivel_2(screen, mapa_niveles)  # Inicia Nivel 2
                        elif i == 3:
                            nivel_3(screen, mapa_niveles)  # Inicia Nivel 3

        pygame.display.update()
