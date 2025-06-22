# operacoes_morfologicas.py
import cv2
import numpy as np


def aplicar_erosao(imagem):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(imagem, kernel, iterations=1)


def aplicar_dilatacao(imagem):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(imagem, kernel, iterations=1)
