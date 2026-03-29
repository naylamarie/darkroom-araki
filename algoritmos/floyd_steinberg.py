import numpy as np
from PIL import Image

def floyd_steinberg(pixels, height, width, umbral):
    # Recorremos cada píxel de la imagen
    p = pixels.copy()
    for y in range(height):
        for x in range(width):
            # Guardamos el valor original del píxel
            original = p[y, x]
            # Lo convertimos a blanco o negro según el umbral
            nuevo = 255 if original > umbral else 0
            p[y, x] = nuevo
            # Calculamos el error — diferencia entre el original y el nuevo valor
            error = original - nuevo
            # Distribuimos el error a los píxeles vecinos
            if x + 1 < width:
                p[y, x + 1] += error * 0.4375       # derecha
            if y + 1 < height:
                p[y + 1, x] += error * 0.1875        # abajo
            if y + 1 < height and x + 1 < width:
                p[y + 1, x + 1] += error * 0.0625   # diagonal
            if y + 1 < height and x - 1 >= 0:
                p[y + 1, x - 1] += error * 0.3125   # abajo izquierda
    return Image.fromarray(np.clip(p, 0, 255).astype(np.uint8))