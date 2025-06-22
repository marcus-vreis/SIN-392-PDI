import matplotlib.pyplot as plt


def criar_grafico_histograma(imagem):
    figura, eixo = plt.subplots()
    eixo.hist(imagem.ravel(), 256, [0, 256])
    eixo.set_title("Histograma da Imagem")
    eixo.set_xlabel("Intensidade do Pixel")
    eixo.set_ylabel("Frequência")
    return figura
