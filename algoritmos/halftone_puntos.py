import numpy as np
from PIL import Image, ImageDraw

def halftone_puntos(pixels, height, width, bloque):
    # Creamos una imagen nueva en blanco para dibujar los puntos
    p = pixels.copy().astype(np.uint8)
    resultado = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(resultado)
    for y in range(0, height, bloque):
        for x in range(0, width, bloque):
            # Extraemos el bloque actual y calculamos su brillo promedio
            celda = p[y:y + bloque, x:x + bloque]
            brillo = np.mean(celda)
            # Negro (0) → círculo grande | Blanco (255) → círculo pequeño
            radio = int((1 - brillo / 255) * (bloque // 2))
            # Calculamos el centro del bloque y dibujamos el círculo
            cx = x + bloque // 2
            cy = y + bloque // 2
            draw.ellipse([cx - radio, cy - radio, cx + radio, cy + radio], fill=0)
    return resultado