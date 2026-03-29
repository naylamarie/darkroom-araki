import numpy as np
from PIL import Image

def bayer(pixels, height, width):
    # Matriz de Bayer 4x4 — grilla de umbrales predefinidos matemáticamente
    # Se repite como mosaico sobre toda la imagen
    matriz = np.array([
        [ 0,  8,  2, 10],
        [12,  4, 14,  6],
        [ 3, 11,  1,  9],
        [15,  7, 13,  5]
    ]) / 16.0 * 255
    p = pixels.copy()
    resultado = np.zeros_like(p)
    for y in range(height):
        for x in range(width):
            # El % hace que la matriz se repita como mosaico
            # Comparamos cada píxel contra el umbral de la matriz en esa posición
            resultado[y, x] = 255 if p[y, x] > matriz[y % 4, x % 4] else 0
    return Image.fromarray(resultado.astype(np.uint8))