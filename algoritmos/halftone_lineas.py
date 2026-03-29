import numpy as np
from PIL import Image, ImageDraw

def halftone_lineas(pixels, height, width, bloque):
    # Creamos una imagen nueva en blanco para dibujar las líneas
    p = pixels.copy().astype(np.uint8)
    resultado = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(resultado)
    for y in range(0, height, bloque):
        for x in range(0, width, bloque):
            # Extraemos el bloque actual y calculamos su brillo promedio
            celda = p[y:y + bloque, x:x + bloque]
            brillo = np.mean(celda)
            # Negro (0) → línea ancha | Blanco (255) → línea fina
            ancho_linea = int((1 - brillo / 255) * bloque)
            # Dibujamos la línea vertical centrada en el bloque
            centro = x + bloque // 2
            x1 = centro - ancho_linea // 2
            x2 = centro + ancho_linea // 2
            draw.rectangle([x1, y, x2, y + bloque], fill=0)
    return resultado