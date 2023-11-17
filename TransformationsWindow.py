import tkinter as tk
from tkinter import ttk

class windowTransformationsObject:
    def __init__(self, masterWindowInstance, index):
        self.options = ["Translação", "Escala", "Rotação", "Cisalhamento", "Reflexão"]

        self.index = index

        self.masterWindowInstance = masterWindowInstance
        self.windowCreate = tk.Toplevel()
        self.windowCreate.title('Menu de Transformação')  

        self.nameLabel = tk.Label(self.windowCreate, text="Transformação")
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10)

        self.selection = ttk.Combobox(self.windowCreate, values=self.options)
        self.selection.grid(row=0, column=1, padx=10, pady=10)
        self.selection.bind("<<ComboboxSelected>>", self.updateOptions)

        self.options_menu_frame = tk.Frame(self.windowCreate)
        self.options_menu_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.updateOptions(None)

        self.buttonCancel = tk.Button(self.windowCreate, text="Cancelar", command=self.windowCreate.destroy)
        self.buttonCancel.grid(row=2, column=0, padx=10, pady=10)

        self.buttonApply = tk.Button(self.windowCreate, text="Aplicar", command=self.updateObject)
        self.buttonApply.grid(row=2, column=3, padx=10, pady=10)

    def optionsMenu(self, optionSelected):
        if optionSelected == "Translação":
            labelX = tk.Label(self.options_menu_frame, text="Deslocamento X:")
            labelX.grid(row=0, column=0, padx=5, pady=5)
            self.entryX = tk.Entry(self.options_menu_frame)
            self.entryX.grid(row=0, column=1, padx=5, pady=5)
            labelY = tk.Label(self.options_menu_frame, text="Deslocamento Y:")
            labelY.grid(row=1, column=0, padx=5, pady=5)
            self.entryY = tk.Entry(self.options_menu_frame)
            self.entryY.grid(row=1, column=1, padx=5, pady=5)

        elif optionSelected == "Escala":
            labelEscalaX = tk.Label(self.options_menu_frame, text="Fator de Escala em X:")
            labelEscalaX.grid(row=0, column=0, padx=5, pady=5)
            self.entryEscalaX = tk.Entry(self.options_menu_frame)
            self.entryEscalaX.grid(row=0, column=1, padx=5, pady=5)
            labelEscalaY = tk.Label(self.options_menu_frame, text="Fator de Escala em Y:")
            labelEscalaY.grid(row=1, column=0, padx=5, pady=5)
            self.entryEscalaY = tk.Entry(self.options_menu_frame)
            self.entryEscalaY.grid(row=1, column=1, padx=5, pady=5)

        elif optionSelected == "Rotação":
            label_angulo = tk.Label(self.options_menu_frame, text="Ângulo de Rotação (°):")
            label_angulo.grid(row=0, column=0, padx=5, pady=5)
            self.entryAngulo = tk.Entry(self.options_menu_frame)
            self.entryAngulo.grid(row=0, column=1, padx=5, pady=5)

        elif optionSelected == "Cisalhamento":
            labelCisalhamentoX = tk.Label(self.options_menu_frame, text="Fator de Cissalhamento em X:")
            labelCisalhamentoX.grid(row=0, column=0, padx=5, pady=5)
            self.entryCisalhamentoX = tk.Entry(self.options_menu_frame)
            self.entryCisalhamentoX.grid(row=0, column=1, padx=5, pady=5)
            labelCisalhamentoY = tk.Label(self.options_menu_frame, text="Fator de Cisalhamento em Y:")
            labelCisalhamentoY.grid(row=1, column=0, padx=5, pady=5)
            self.entryCisalhamentoY = tk.Entry(self.options_menu_frame)
            self.entryCisalhamentoY.grid(row=1, column=1, padx=5, pady=5)

        elif optionSelected == "Reflexão":
            labelReflexao = tk.Label(self.options_menu_frame, text="Escolha a Reflexão:")
            labelReflexao.grid(row=0, column=0, padx=5, pady=5)
            self.selectionReflexao = ttk.Combobox(self.options_menu_frame, values=["Vertical", "Horizontal"])
            self.selectionReflexao.grid(row=0, column=1, padx=5, pady=5)

    def updateOptions(self, event):
        self.optionSelected = self.selection.get()
        for widget in self.options_menu_frame.winfo_children():
            widget.destroy()
        self.optionsMenu(self.optionSelected)

    def updateObject(self):
        option = self.optionSelected
        obj = self.masterWindowInstance.ListObjects[self.index]
        obj.Undraw()
        self.masterWindowInstance.canvas.draw()

        if option == "Translação":
            x, y = float(self.entryX.get()), float(self.entryY.get())
            obj.Translate(x, y)
        elif option == "Escala":
            x, y = float(self.entryEscalaX.get()), float(self.entryEscalaY.get())
            obj.Scale(x, y)
        elif option == "Rotação":
            angulo = float(self.entryAngulo.get())
            obj.Rotate(angulo)
        elif option == "Cisalhamento":
            x, y  = float(self.entryCisalhamentoX.get()), float(self.entryCisalhamentoY.get())
            obj.Shear(x, y)
        elif option == "Reflexão":
            reflexao = self.selectionReflexao.get()
            obj.Reflect(reflexao)
        
        obj.listScatter = []
        scatters = []

        for v in obj.listVertex:
            scatter = self.masterWindowInstance.ax.scatter(v[0], v[1], color = 'blue')
            scatters.append(scatter)
            self.masterWindowInstance.canvas.draw()
        
        obj.listScatter = scatters

        self.masterWindowInstance.update_canva(index=self.index)
        self.windowCreate.destroy()