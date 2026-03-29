import numpy as np
from PIL import Image

def threshold(pixels, height, width, umbral):
    # Corte directo sin distribución de error
    # Todo lo que supera el umbral es blanco, lo demás negro
    p = np.where(pixels > umbral, 255, 0)
    return Image.fromarray(p.astype(np.uint8))