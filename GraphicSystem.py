import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CreateObjectWindow import windowCreateObject
from TransformationsWindow import windowTransformationsObject
from tkinter import colorchooser
from ObjectFromFile import GetObjectFromFile

# Janela Principal
class windowMaster:
    def __init__(self, master):
        self.master = master
        master.geometry("1280x720")
        master.title("Graph Application")

        self.configure_layout()

        self.config_canva()

        self.ListObjects = []
        self.listOfNewPolygonPoints = []
        self.listOfNewPolygonVertexes = []
        self.createMode = False
        self.mouse_is_pressed = False
        self.last_press = None

        self.canvas.mpl_connect("button_press_event", self.on_mouse_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_drag)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_release)
        self.canvas.mpl_connect("scroll_event", self.on_mouse_scroll)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)

    def configure_layout(self):
        # Configuração do gráfico
        self.figure, self.ax = Figure(), None
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Container para layout direito
        self.frame = tk.Frame(self.master, background='#F0F2F3')
        self.frame.grid(row=0, column=1, sticky='nsew')

        # Configuração do layout do frame direito
        self.frame.grid_rowconfigure(2, weight=18)  # 80% da altura
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Botões
        self.buttonOpenFile = tk.Button(self.frame, text="Abrir arquivo (.obj)", command=self.on_openfile_click)
        self.buttonOpenFile.grid(row=0, column=0, padx=10, pady=10)

        self.buttonCreateObject = tk.Button(self.frame, text="Criar Objeto", command=self.on_buttoncreateobject_click)
        self.buttonCreateObject.grid(row=1, column=0, padx=10, pady=10)

        # Lista de objetos
        self.displayFile = tk.Listbox(self.frame)
        self.displayFile.grid(row=2, column=0, padx=30, pady=10, sticky='nsew')

        # Scroll ao lado da lista de objetos
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.displayFile.yview)
        scrollbar.grid(row=2, column=1, sticky='ns')
        self.displayFile.config(yscrollcommand=scrollbar.set)

        # Configuração do layout do frame
        self.master.grid_columnconfigure(0, weight=3)
        self.master.grid_columnconfigure(1, weight=1)  
        self.master.grid_rowconfigure(0, weight=1)

    def config_canva(self):        
        if self.ax:
            self.ax.clear()

        self.ax = self.figure.add_subplot(111)

        self.ax.grid(True, linestyle='-', alpha=0.5) 

        self.ax.axhline(0, color='black', lw=2)  # Linha horizontal no eixo x
        self.ax.axvline(0, color='black', lw=2)  # Linha vertical no eixo y

        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        self.canvas.draw()

    def update_canva(self, index = -1):
        obj = self.ListObjects[index]
        polygon = obj.polygon
        patch = self.ax.add_patch(polygon)

        obj.SetPatch(patch)

        self.canvas.draw()

    def round_to_nearest_01(self, number):
        rounded_number = round(number * 10) / 10  # Arredonda para o valor mais próximo com uma casa decimal
        return rounded_number

    def on_mouse_press(self, event):
        # Move o plano cartesiano com o mouse
        if event.inaxes:
            self.last_press = (event.xdata, event.ydata)
        self.mouse_is_pressed = True

        if self.createMode:
            x, y = (self.round_to_nearest_01(event.xdata), self.round_to_nearest_01(event.ydata))
            self.listOfNewPolygonVertexes.append((x, y))
            scatter = self.ax.scatter(x, y, color='blue')
            self.listOfNewPolygonPoints.append(scatter)
            self.canvas.draw()
    
    def on_key_press(self, event):
        if event.key == 'enter' and self.createMode:
            self.createMode = False
            windowCreateObject(self)
        elif event.key == 'escape' and self.createMode:
            self.cancel_creation()

    
    def cancel_creation(self):
        for p in self.listOfNewPolygonPoints:
            p.remove()
        self.listOfNewPolygonPoints = []
        self.createMode = False
        self.canvas.draw()

        self.buttonCreateObject.config(state=tk.NORMAL)

        self.buttonOpenFile.config(state=tk.NORMAL)

    def on_mouse_release(self, event):
        self.mouse_is_pressed = False

    def on_mouse_drag(self, event):
        if not self.last_press or not self.mouse_is_pressed:
            return

        # Move o plano cartesiano com o mouse
        if self.last_press and event.inaxes:
            dx = event.xdata - self.last_press[0]
            dy = event.ydata - self.last_press[1]

            dx, dy = dx*0.6, dy*0.6

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

    def on_openfile_click(self):
        self.buttonCreateObject.config(state=tk.DISABLED)
        self.buttonOpenFile.config(state=tk.DISABLED)

        color = colorchooser.askcolor(parent=self.master ,title="Escolha uma cor")[1]
        file_path = tk.filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos .obj", "*.obj")] )

        if file_path:
            obj = GetObjectFromFile(file_path, color)
            for v in obj.listVertex:
                scatter = self.ax.scatter(v[0], v[1], color='blue')
                obj.listScatter.append(scatter)
                if obj == None: 
                    tk.messagebox.showerror("Erro", "Arquivo inválido.", parent=self.master)
                    return
                self.canvas.draw()

            self.ListObjects.append(obj)

            self.update_listbox(obj.name)
            self.update_canva()
        else:
            tk.messagebox.showerror("Erro", "Arquivo inválido.", parent=self.master)

        self.buttonCreateObject.config(state=tk.NORMAL)
        self.buttonOpenFile.config(state=tk.NORMAL)

    def on_buttoncreateobject_click(self):
        self.createMode = True
        self.buttonCreateObject.config(state=tk.DISABLED) 
        self.buttonOpenFile.config(state=tk.DISABLED)

    def update_listbox(self, info):
        self.displayFile.insert(tk.END, info) 
        self.displayFile.bind("<Button-3>", self.on_listbox_right_click)

    def delete(self, index):
        object = self.ListObjects[index]
        object.Undraw()

        self.ListObjects.remove(object)
        self.displayFile.delete(index)
        self.canvas.draw()

    def on_listbox_right_click(self, event):
        # Pega o índice do item clicado
        item_index = self.displayFile.nearest(event.y)

        # Obtém as coordenadas do clique
        x, y, _, _ = self.displayFile.bbox(item_index)

        # Converte as coordenadas para a posição da janela principal
        x_root = self.displayFile.winfo_rootx() + x
        y_root = self.displayFile.winfo_rooty() + y

        # Cria o menu de contexto
        self.menu = tk.Menu(self.master, tearoff=0)
        self.menu.add_command(label="Deletar", command=lambda: self.delete(item_index))
        self.menu.add_command(label="Aplicar Transformação", command=lambda: self.open_window_transformation(item_index))

        # Exibe o menu de contexto
        self.menu.post(x_root, y_root)

        self.master.bind("<Button-1>", self.close_menu_on_mouse_button)
    
    def open_window_transformation(self, index):
        windowTransformationsObject(self, index)

    def close_menu_on_mouse_button(self, event):
        # Verifica se o menu de contexto existe antes de tentar destruí-lo
        if hasattr(self, 'menu') and self.menu:
            self.menu.destroy()

def main():          
    root = tk.Tk()
    app = windowMaster(root)
    root.mainloop()

if __name__ == "__main__":
    main()