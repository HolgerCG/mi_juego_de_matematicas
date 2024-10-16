# acercade.py
import os
import pygame
import sys

# Función para obtener la ruta completa de un recurso (si no está en compartido.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def obtener_ruta_recurso(ruta_relativa):
    return os.path.join(BASE_DIR, ruta_relativa)

# Función para mostrar la pantalla de "Acerca de"
def mostrar_acerca_de(screen):
    # Colores mejorados
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 200)
    LIGHT_BLUE = (135, 206, 250)  # Azul claro para hover en el botón
    BLACK = (0, 0, 0)
    GREY = (50, 50, 50)

    # Fuentes
    font = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
    small_font = pygame.font.SysFont("Comic Sans MS", 24)

    # Texto que se mostrará
    titulo = "Acerca de MATEBOT"
    descripcion = [
        "MATEBOT es un robot interactivo creado para el apoyo",
        "en la enseñanza de MATEMATICAS a niños pequeños.",
        "Responde preguntas y brinda apoyo didáctico.",
        "Autor: Holger Centeno.",
        "Bajo la dirección del Ing. Orlando Erazo, PhD.",
        "Hecho con Python y Pygame."
    ]

    # Fondo con un color degradado mejorado
    for y in range(screen.get_height()):
        color_gradiente = (
            int(255 - (y / screen.get_height()) * 100),  # Más sutil en el degradado
            int(255 - (y / screen.get_height()) * 100),
            255
        )
        pygame.draw.line(screen, color_gradiente, (0, y), (screen.get_width(), y))

    # Renderizar título con sombra
    shadow_offset = 2
    titulo_surf_shadow = font.render(titulo, True, GREY)
    titulo_rect_shadow = titulo_surf_shadow.get_rect(center=(screen.get_width() // 2 + shadow_offset, 100 + shadow_offset))
    screen.blit(titulo_surf_shadow, titulo_rect_shadow)

    titulo_surf = font.render(titulo, True, BLUE)
    titulo_rect = titulo_surf.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(titulo_surf, titulo_rect)

    # Renderizar descripción con mayor margen en la parte inferior
    y_offset = 180  # Donde empieza el texto de descripción
    line_spacing = 35  # Ajustar espacio entre líneas
    for linea in descripcion:
        linea_surf = small_font.render(linea, True, BLACK)
        linea_rect = linea_surf.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(linea_surf, linea_rect)
        y_offset += line_spacing  # Ajustar espacio entre líneas

    # Botón de "Regresar" con bordes redondeados y mejor posicionado
    boton_rect = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() - 80, 200, 50)  # Posición ajustada
    pygame.draw.rect(screen, BLUE, boton_rect, border_radius=12)  # Bordes redondeados
    boton_texto = small_font.render("Regresar", True, WHITE)
    boton_texto_rect = boton_texto.get_rect(center=boton_rect.center)
    screen.blit(boton_texto, boton_texto_rect)

    pygame.display.flip()

    # Bucle para esperar interacción del usuario para regresar al menú principal
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    esperando = False  # Salir de la pantalla de "Acerca de" y regresar al menú principal

        # Hover en el botón
        mouse_pos = pygame.mouse.get_pos()
        if boton_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT_BLUE, boton_rect, border_radius=12)
        else:
            pygame.draw.rect(screen, BLUE, boton_rect, border_radius=12)

        screen.blit(boton_texto, boton_texto_rect)
        pygame.display.flip()
