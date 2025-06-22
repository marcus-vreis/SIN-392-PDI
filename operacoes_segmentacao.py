import cv2


def aplicar_limiar_otsu(imagem):
    _, imagem_limiarizada = cv2.threshold(
        imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return imagem_limiarizada
