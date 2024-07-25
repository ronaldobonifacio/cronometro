import tkinter as tk
from PIL import Image, ImageTk
import time

class Cronometro:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.tempo_restante = 0
        self.rodando = False
        self.widgets_ocultos = False

        # Adiciona o ícone da janela
        self.icon = Image.open('./src/image/clock.png')  # Substitua pelo caminho para o seu arquivo de imagem
        self.icon = self.icon.resize((32, 32))  # Redimensiona para 32x32 pixels
        self.icon_photo = ImageTk.PhotoImage(self.icon)
        self.root.iconphoto(False, self.icon_photo)
        
        # Remove o botão de minimizar
        self.root.attributes('-toolwindow', True)
        self.root.attributes('-topmost', True)
        
        # Define a fonte como negrito
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 35, "bold"), fg="blue")
        self.label.grid(row=0, column=0, columnspan=2, padx=0, pady=0)
        self.label.bind("<Double-1>", self.toggle_widgets)

        self.frame_entrada = tk.Frame(root)
        self.frame_entrada.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.label_entrada = tk.Label(self.frame_entrada, text="Tempo (min):")
        self.label_entrada.grid(row=0, column=0, padx=5, pady=5)

        # Ajuste a largura do campo de entrada de minutos
        self.entrada_minutos = tk.Entry(self.frame_entrada, width=10)  # Ajuste o valor de largura conforme necessário
        self.entrada_minutos.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_minutos.insert(0, "Minutos")

        self.iniciar_pausar_button = tk.Button(root, text="Iniciar", command=self.iniciar_pausar)
        self.iniciar_pausar_button.grid(row=2, column=0, padx=10, pady=5)

        self.resetar_button = tk.Button(root, text="Resetar", command=self.resetar)
        self.resetar_button.grid(row=2, column=1, padx=10, pady=5)

        # Configurar redimensionamento
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.root.minsize(0, 0)

    def iniciar_pausar(self):
        if self.rodando:
            self.parar()
        else:
            self.iniciar()

    def iniciar(self):
        try:
            if not self.rodando:
                minutos = int(self.entrada_minutos.get())
                self.tempo_restante = minutos * 60 if self.tempo_restante == 0 else self.tempo_restante
                self.rodando = True
                self.iniciar_pausar_button.config(text="Pausar")
                self.ocultar_widgets()
                self.atualizar_tempo()
        except ValueError:
            self.label.config(text="Entrada inválida")

    def parar(self):
        self.rodando = False
        self.iniciar_pausar_button.config(text="Iniciar")
        self.exibir_widgets()

    def resetar(self):
        self.rodando = False
        self.tempo_restante = 0
        self.label.config(text="00:00:00", fg="blue")
        self.iniciar_pausar_button.config(text="Iniciar")
        if self.widgets_ocultos:
            self.exibir_widgets()

    def ocultar_widgets(self):
        if not self.widgets_ocultos:
            self.frame_entrada.grid_remove()
            self.iniciar_pausar_button.grid_remove()
            self.resetar_button.grid_remove()
            # Ajusta a altura da janela quando apenas o cronômetro é exibido
            self.root.geometry(f"200x50")  # Ajuste a largura e altura conforme necessário
            self.widgets_ocultos = True

    def exibir_widgets(self):
        if self.widgets_ocultos:
            self.frame_entrada.grid()
            self.iniciar_pausar_button.grid()
            self.resetar_button.grid()
            # Ajusta a altura da janela para incluir todos os widgets
            self.root.geometry("")  # Ajuste a geometria para o tamanho necessário
            self.widgets_ocultos = False

    def toggle_widgets(self, event):
        if self.widgets_ocultos:
            self.exibir_widgets()
        else:
            self.ocultar_widgets()

    def atualizar_tempo(self):
        if self.rodando:
            if self.tempo_restante > 0:
                self.tempo_restante -= 1
                self.label.config(fg="blue")
            elif self.tempo_restante == 0:
                self.label.config(fg="red")
                self.tempo_restante -= 1
            else:
                self.tempo_restante -= 1
                self.label.config(fg="red")

            tempo_str = time.strftime('%H:%M:%S', time.gmtime(abs(self.tempo_restante)))
            self.label.config(text=tempo_str)
            self.root.after(1000, self.atualizar_tempo)

root = tk.Tk()
cronometro = Cronometro(root)
root.mainloop()
