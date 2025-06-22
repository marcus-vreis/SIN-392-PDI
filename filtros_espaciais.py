import cv2
import numpy as np
from skimage.filters import roberts, prewitt


def aplicar_filtro_media(imagem):
    return cv2.blur(imagem, (5, 5))


def aplicar_filtro_mediana(imagem):
    return cv2.medianBlur(imagem, 5)


def aplicar_filtro_gaussiano(imagem):
    return cv2.GaussianBlur(imagem, (5, 5), 0)


def aplicar_filtro_laplaciano(imagem):
    laplaciano = cv2.Laplacian(imagem, cv2.CV_64F)
    return cv2.convertScaleAbs(laplaciano)


def aplicar_filtro_sobel(imagem):
    sobel_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=5)
    return cv2.convertScaleAbs(np.sqrt(sobel_x**2 + sobel_y**2))


def aplicar_filtro_prewitt(imagem):
    resultado = prewitt(imagem)
    resultado = (resultado - resultado.min()) / \
        (resultado.max() - resultado.min()) * 255
    return resultado.astype(np.uint8)


def aplicar_filtro_roberts(imagem):
    resultado = roberts(imagem)
    resultado = (resultado - resultado.min()) / \
        (resultado.max() - resultado.min()) * 255
    return resultado.astype(np.uint8)
