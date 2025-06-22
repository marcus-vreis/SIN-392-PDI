import tkinter as tk
from tkinter import filedialog, Frame, Label, Button
from PIL import Image, ImageTk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import operacoes_histograma
import transformacoes_intensidade
import filtros_espaciais
import dominio_frequencia
import operacoes_morfologicas
import operacoes_segmentacao


class processadordeimagens:
    def __init__(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("Filtrador de Imagens")
        self.janela.geometry("1280x720")

        self.imagem_original = None
        self.imagem_processada = None

        frame_controles = Frame(self.janela)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        frame_imagens = Frame(self.janela)
        frame_imagens.pack(side=tk.RIGHT, expand=True,
                           fill=tk.BOTH, padx=10, pady=10)

        self.label_original = Label(frame_imagens, text="Imagem Original")
        self.label_original.pack(
            side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

        self.label_processada = Label(frame_imagens, text="Imagem Processada")
        self.label_processada.pack(
            side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

        Button(frame_controles, text="Carregar Imagem",
               command=self.carregar_imagem).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Salvar Imagem Processada",
               command=self.salvar_imagem).pack(fill=tk.X, pady=2)

        Label(frame_controles).pack(pady=5)  # Um pequeno espaço

        Button(frame_controles, text="Exibir Histograma",
               command=self.executar_mostrar_histograma).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Alargamento de Contraste", command=lambda: self._processar_e_exibir(
            transformacoes_intensidade.alargamento_contraste)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Equalização de Histograma", command=lambda: self._processar_e_exibir(
            transformacoes_intensidade.equalizacao_histograma)).pack(fill=tk.X, pady=2)

        Label(frame_controles).pack(pady=5)

        Button(frame_controles, text="Filtro de Média", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_media)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Filtro de Mediana", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_mediana)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Filtro Gaussiano", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_gaussiano)).pack(fill=tk.X, pady=2)

        Label(frame_controles).pack(pady=5)

        Button(frame_controles, text="Filtro Laplaciano", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_laplaciano)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Filtro Sobel", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_sobel)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Filtro Prewitt", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_prewitt)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Filtro Roberts", command=lambda: self._processar_e_exibir(
            filtros_espaciais.aplicar_filtro_roberts)).pack(fill=tk.X, pady=2)

        Label(frame_controles).pack(pady=5)

        Button(frame_controles, text="Filtro Freq. Passa-Baixa", command=lambda: self._processar_e_exibir(
            lambda img: dominio_frequencia.aplicar_filtro_frequencia(img, "passa-baixa"))).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Filtro Freq. Passa-Alta", command=lambda: self._processar_e_exibir(
            lambda img: dominio_frequencia.aplicar_filtro_frequencia(img, "passa-alta"))).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Espectro de Fourier", command=lambda: self._processar_e_exibir(
            dominio_frequencia.obter_espectro_fourier)).pack(fill=tk.X, pady=2)

        Label(frame_controles).pack(pady=5)

        Button(frame_controles, text="Erosão", command=lambda: self._processar_e_exibir(
            operacoes_morfologicas.aplicar_erosao)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Dilatação", command=lambda: self._processar_e_exibir(
            operacoes_morfologicas.aplicar_dilatacao)).pack(fill=tk.X, pady=2)
        Button(frame_controles, text="Limiar de Otsu", command=lambda: self._processar_e_exibir(
            operacoes_segmentacao.aplicar_limiar_otsu)).pack(fill=tk.X, pady=2)

        Button(frame_controles, text="Resetar Imagem", command=self.resetar_imagem).pack(
            fill=tk.X, side=tk.BOTTOM, pady=10)

    def _exibir_imagem(self, dados_imagem, label_widget):
        imagem_pil = Image.fromarray(dados_imagem)

        largura, altura = imagem_pil.size
        if largura > 550 or altura > 550:
            imagem_pil.thumbnail((550, 550))

        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        label_widget.config(image=imagem_tk)
        label_widget.image = imagem_tk

    def _processar_e_exibir(self, funcao_processamento):
        if self.imagem_original is None:
            print("Erro: Nenhuma imagem carregada.")
            return
        self.imagem_processada = funcao_processamento(self.imagem_original)
        self._exibir_imagem(self.imagem_processada, self.label_processada)

    def carregar_imagem(self):
        caminho_arquivo = filedialog.askopenfilename()
        if not caminho_arquivo:
            return

        imagem_colorida = cv2.imread(caminho_arquivo)
        self.imagem_original = cv2.cvtColor(
            imagem_colorida, cv2.COLOR_BGR2GRAY)

        self.resetar_imagem()

    def salvar_imagem(self):
        if self.imagem_processada is None:
            return
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")])
        if not caminho_arquivo:
            return
        cv2.imwrite(caminho_arquivo, self.imagem_processada)

    def resetar_imagem(self):
        if self.imagem_original is not None:
            self.imagem_processada = self.imagem_original.copy()
            self._exibir_imagem(self.imagem_original, self.label_original)
            self._exibir_imagem(self.imagem_processada, self.label_processada)

    def executar_mostrar_histograma(self):
        if self.imagem_processada is None:
            return

        nova_janela = tk.Toplevel(self.janela)
        nova_janela.title("Histograma")

        figura = operacoes_histograma.criar_grafico_histograma(
            self.imagem_processada)

        canvas = FigureCanvasTkAgg(figura, master=nova_janela)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    janela_raiz = tk.Tk()
    app = processadordeimagens(janela_raiz)
    janela_raiz.mainloop()
