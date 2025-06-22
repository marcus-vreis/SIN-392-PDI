import cv2


def alargamento_contraste(imagem):
    return cv2.normalize(imagem, None, 0, 255, cv2.NORM_MINMAX)


def equalizacao_histograma(imagem):
    return cv2.equalizeHist(imagem)
