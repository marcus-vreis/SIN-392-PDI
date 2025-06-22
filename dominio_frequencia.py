import cv2
import numpy as np


def _criar_mascara(formato, raio, tipo_filtro="passa-baixa"):
    linhas, colunas = formato
    centro_linha, centro_coluna = linhas // 2, colunas // 2

    mascara = np.zeros((linhas, colunas), np.uint8)
    x, y = np.ogrid[:linhas, :colunas]
    area_mascara = (x - centro_linha)**2 + (y - centro_coluna)**2 <= raio*raio

    if tipo_filtro == "passa-baixa":
        mascara[area_mascara] = 1
    elif tipo_filtro == "passa-alta":
        mascara = np.ones((linhas, colunas), np.uint8)
        mascara[area_mascara] = 0
    return mascara


def aplicar_filtro_frequencia(imagem, tipo_filtro="passa-baixa"):
    dft = cv2.dft(np.float32(imagem), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    mascara = _criar_mascara(imagem.shape, raio=30, tipo_filtro=tipo_filtro)

    fshift = dft_shift * np.stack([mascara, mascara], axis=-1)

    f_ishift = np.fft.ifftshift(fshift)
    img_retorno = cv2.idft(f_ishift)
    img_retorno = cv2.magnitude(img_retorno[:, :, 0], img_retorno[:, :, 1])

    cv2.normalize(img_retorno, img_retorno, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(img_retorno)


def obter_espectro_fourier(imagem):
    dft = cv2.dft(np.float32(imagem), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    espectro = 20 * \
        np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)

    cv2.normalize(espectro, espectro, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(espectro)
