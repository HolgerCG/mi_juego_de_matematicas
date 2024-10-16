import os
import pygame
import sys

# Determina el directorio base del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Función para obtener la ruta completa de un recurso
def obtener_ruta_recurso(ruta_relativa):
    return os.path.join(BASE_DIR, ruta_relativa)

# Función compartida para mostrar texto centrado
def mostrar_texto_centrado(texto, fuente, color, rect, screen):
    superficie = fuente.render(texto, True, color)
    texto_rect = superficie.get_rect()
    texto_rect.center = (rect.x + rect.width // 2, rect.y + rect.height // 2 + 5)  # Centrado con ajuste
    screen.blit(superficie, texto_rect)
