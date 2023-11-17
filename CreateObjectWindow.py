from tkinter import colorchooser
import tkinter as tk
from Object import Object

class windowCreateObject:
    def __init__(self, masterWindowInstance):
        # Função a ser executada quando o Botão de criação de objeto é clicado
        self.masterWindowInstance = masterWindowInstance

        self.windowCreate = tk.Toplevel()
        self.windowCreate.title('Criação de objetos')

        self.windowCreate.protocol("WM_DELETE_WINDOW", self.on_close)

        self.color = 'cyan'    

        self.nameLabel = tk.Label(self.windowCreate,text="Nome")
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.entryName = tk.Entry(self.windowCreate)
        self.entryName.grid(row=0, column=2, padx=10, pady=10, columnspan=2)

        self.buttonColor = tk.Button(self.windowCreate, text="Escolher Cor", command=self.getColor)
        self.buttonColor.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.colorCanvas = tk.Canvas(self.windowCreate, width=20, height=20, bg=self.color, highlightthickness=0)
        self.colorCanvas.grid(row=1, column=2, padx=10, pady=10)

        self.buttonCreate = tk.Button(self.windowCreate, text="Criar", command=self.createObject)
        self.buttonCreate.grid(row=1, column=3, padx=10, pady=10)
    
    def on_close(self):
        self.masterWindowInstance.cancel_creation()
        self.windowCreate.destroy()

    def getColor(self):
        color = colorchooser.askcolor(parent=self.windowCreate ,title="Escolha uma cor")[1]
        if color:
            self.color = color
        self.colorCanvas.config(bg = self.color)

    def createObject(self):
        name = self.entryName.get()

        if name == "":
            tk.messagebox.showerror("Erro", "O nome do objeto não pode ser vazio.", parent=self.windowCreate)
            return

        if len(self.masterWindowInstance.listOfNewPolygonVertexes) <= 1:
            tk.messagebox.showerror("Erro", "O objeto não pode ser vazio.", parent=self.windowCreate)
            return
        
        new_object = Object(name, self.masterWindowInstance.listOfNewPolygonVertexes, self.masterWindowInstance.listOfNewPolygonPoints, self.color)
        self.masterWindowInstance.ListObjects.append(new_object)

        self.masterWindowInstance.update_listbox(new_object.name)

        self.masterWindowInstance.listOfNewPolygonVertexes = []

        self.masterWindowInstance.listOfNewPolygonPoints = []

        self.masterWindowInstance.update_canva()

        self.masterWindowInstance.buttonCreateObject.config(state=tk.NORMAL)

        self.masterWindowInstance.buttonOpenFile.config(state=tk.NORMAL)

        self.windowCreate.destroy()