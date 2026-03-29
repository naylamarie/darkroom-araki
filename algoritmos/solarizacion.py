import numpy as np
from PIL import Image

def solarizacion(pixels, height, width, umbral):
    # Copiamos los píxeles para no modificar la imagen original
    p = pixels.copy()
    for y in range(height):
        for x in range(width):
            # Si el píxel supera el umbral lo invertimos — 255 - valor
            # Si no supera el umbral lo dejamos igual
            # Esto crea el efecto de inversión parcial 
            if p[y, x] > umbral:
                p[y, x] = 255 - p[y, x]
    return Image.fromarray(np.clip(p, 0, 255).astype(np.uint8))