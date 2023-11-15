import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import Object

ListObjects = []

# Janela Principal
class windowMaster:
    def __init__(self, master):
        self.master = master
        master.geometry("1280x720")
        master.title("Graph Application")

        self.configure_layout()

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

        # Container para layout direito
        self.frame = tk.Frame(self.master, background='#F0F2F3')
        self.frame.grid(row=0, column=1, sticky='nsew')

         # Botões
        self.buttonOpenFile = tk.Button(self.frame, text="Abrir arquivo (.obj)", command=self.on_openfile_click)
        self.buttonOpenFile.pack(pady=10)

        self.buttonCreateObject = tk.Button(self.frame, text="Criar Objeto", command=self.on_buttoncreateobject_click)
        self.buttonCreateObject.pack(pady=10)

        # Lista de objetos
        self.displayFile = tk.Listbox(self.frame)
        self.displayFile.pack(pady=10, padx=30, expand=True, fill=tk.BOTH)        

        # Scroll ao lado da lista de objetos
        scrollbar = tk.Scrollbar(self.displayFile, orient="vertical", command=self.displayFile.yview)
        scrollbar.pack(side="right", fill="y")
        self.displayFile.config(yscrollcommand=scrollbar.set)

    def plot_points(self):        
        if self.ax:
            self.ax.clear()

        self.ax = self.figure.add_subplot(111)

        self.ax.grid(True, linestyle='-', alpha=0.5) 

        self.ax.axhline(0, color='black', lw=2)  # Linha horizontal no eixo x
        self.ax.axvline(0, color='black', lw=2)  # Linha vertical no eixo y

        self.canvas.draw()

    def update_canva(self):

        obj = ListObjects[-1]
        polygon = obj.polygon
        self.ax.add_patch(polygon)

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

    def on_openfile_click(self):
        file_path = tk.filedialog.askopenfilename(title="Selecione um arquivo")
        if file_path:
            print("Arquivo selecionado:", file_path)

    def on_buttoncreateobject_click(self):
        windowCreateObject(self)    

    def update_listbox(self, info):
        self.displayFile.insert(tk.END, info) 
        self.displayFile.bind("<Button-3>", self.on_listbox_right_click)

    def menu_command(self, index, option):
        print(f"Item {index} selecionado. Opção escolhida: {option}")   

    def on_listbox_right_click(self, event):
        # Pega o índice do item clicado
        item_index = self.displayFile.nearest(event.y)

        # Obtém as coordenadas do clique
        x, y, _, _ = self.displayFile.bbox(item_index)

        # Converte as coordenadas para a posição da janela principal
        x_root = self.displayFile.winfo_rootx() + x
        y_root = self.displayFile.winfo_rooty() + y

        # Cria o menu de contexto
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="Opção 1", command=lambda: self.menu_command(item_index, "Opção 1"))
        menu.add_command(label="Opção 2", command=lambda: self.menu_command(item_index, "Opção 2"))

        # Exibe o menu de contexto
        menu.post(x_root, y_root)


# janela de criacao de objetos            
class windowCreateObject:
    def __init__(self, masterWindowInstance):
        # Função a ser executada quando o Botão de criação de objeto é clicado
        self.masterWindowInstance = masterWindowInstance

        self.windowCreate = tk.Toplevel()
        self.windowCreate.title('Criação de objetos')    

        self.nameLabel = tk.Label(self.windowCreate,text="Nome")
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.name = tk.Entry(self.windowCreate)
        self.name.grid(row=0, column=1, padx=10, pady=10)

        self.pointsLabel = tk.Label(self.windowCreate,text="Lista de pontos")
        self.pointsLabel.grid(row=1, column=0, padx=10, pady=0)
        self.points = tk.Entry(self.windowCreate)
        self.points.grid(row=1, column=1, padx=10, pady=0)      

        self.pointsLabel = tk.Label(self.windowCreate,text="(x1,y1),(x2,y2),(x3,y3) ...")
        self.pointsLabel.grid(row=2, column=1, padx=10, pady=0)

        self.buttonCreate = tk.Button(self.windowCreate, text="Criar", command=self.createObject)
        self.buttonCreate.grid(row=3, column=0, padx=10, pady=10)

        self.buttonCancel = tk.Button(self.windowCreate, text="Cancelar", command=self.windowCreate.destroy)
        self.buttonCancel.grid(row=3, column=1, padx=10, pady=10)

    def createObject(self):
        name = self.name.get()
        points = self.points.get()
        
        points_str = points.split('),(')              
        VectorPoints = [tuple(map(float, point.strip('()').split(','))) for point in points_str]

        new_object = Object.Object(name, VectorPoints)
        ListObjects.append(new_object)

        self.masterWindowInstance.update_listbox(new_object.name)
        self.masterWindowInstance.update_canva()

        self.windowCreate.destroy()

root = tk.Tk()
app = windowMaster(root)
root.mainloop()