import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon

class GraphApp:
    def __init__(self, master):
        self.master = master
        master.geometry("1280x720")
        master.title("Graph Application")

        self.configure_layout()

        self.points = [(1, 1), (2, 2), (3, 1)]  # Exemplo de pontos

        self.plot_points()

        self.mouse_is_pressed = False
        self.last_press = None

        self.canvas.mpl_connect("button_press_event", self.on_mouse_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_drag)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_release)
        self.canvas.mpl_connect("scroll_event", self.on_mouse_scroll)

    def configure_layout(self):
         # Configuração do layout
        self.master.grid_columnconfigure(0, weight=3)
        self.master.grid_columnconfigure(1, weight=1)  # A segunda coluna não redimensiona
        self.master.grid_rowconfigure(0, weight=1)

        # Configuração do gráfico
        self.figure, self.ax = Figure(), None
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Configuração dos botões
        self.button_frame = tk.Frame(self.master, background='#F0F2F3')
        self.button_frame.grid(row=0, column=1, sticky='nsew')

        self.button1 = tk.Button(self.button_frame, text="Botão 1", command=self.on_button1_click)
        self.button1.pack(pady=10)

        self.button2 = tk.Button(self.button_frame, text="Botão 2", command=self.on_button2_click)
        self.button2.pack(pady=10)



    def plot_points(self):
        if self.ax:
            self.ax.clear()

        self.ax = self.figure.add_subplot(111)

        polygon = Polygon([(1.5, 0.5), (2.5, 0.5), (2.5, 1.5), (1.5, 1.5)], closed=True, edgecolor='blue', facecolor='cyan', alpha=0.5)
        self.ax.add_patch(polygon)

        x, y = zip(*self.points)
        self.ax.scatter(x, y)

        self.ax.grid(True, linestyle='-', alpha=0.5) 

        self.ax.axhline(0, color='black', lw=2)  # Linha horizontal no eixo x
        self.ax.axvline(0, color='black', lw=2)  # Linha vertical no eixo y


        self.canvas.draw()

    def on_mouse_press(self, event):
        # Move o plano cartesiano com o mouse
        if event.inaxes:
            self.last_press = (event.xdata, event.ydata)
        self.mouse_is_pressed = True

    def on_mouse_release(self, event):
        self.mouse_is_pressed = False

    def on_mouse_drag(self, event):
        if not self.last_press or not self.mouse_is_pressed:
            return

        # Move o plano cartesiano com o mouse
        if self.last_press and event.inaxes:
            dx = event.xdata - self.last_press[0]
            dy = event.ydata - self.last_press[1]

            dx, dy = dx*0.7, dy*0.7

            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
            self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)

            self.last_press = (event.xdata, event.ydata)
            self.canvas.draw()

    def on_mouse_scroll(self, event):
        # Dá zoom no plano cartesiano com o scroll do mouse
        if event.inaxes:
            if event.step < 0:
                self.ax.set_xlim(self.ax.get_xlim()[0], self.ax.get_xlim()[1] * 1.1)
                self.ax.set_ylim(self.ax.get_ylim()[0], self.ax.get_ylim()[1] * 1.1)
            else:
                self.ax.set_xlim(self.ax.get_xlim()[0], self.ax.get_xlim()[1] / 1.1)
                self.ax.set_ylim(self.ax.get_ylim()[0], self.ax.get_ylim()[1] / 1.1)

            self.canvas.draw()

    def on_button1_click(self):
        file_path = tk.filedialog.askopenfilename(title="Selecione um arquivo")
        if file_path:
            print("Arquivo selecionado:", file_path)

    def on_button2_click(self):
        # Função a ser executada quando o Botão 2 é clicado
        print("Botão 2 clicado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
