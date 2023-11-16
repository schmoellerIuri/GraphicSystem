import numpy as np
import math
from matplotlib.patches import Polygon

class Object:
    def __init__(self, name, listVertex, listScatter,color='cyan'):
        self.name = name
        self.listVertex = listVertex    
        self.polygon = Polygon(listVertex, closed=True, edgecolor='blue', facecolor=color, alpha=0.5)
        self.listScatter = listScatter

    def Undraw(self):
        self.patch.remove()
        for scatter in self.listScatter:
            scatter.remove()

    def SetPatch(self, scatter):
        self.patch = scatter

    def Translate(x, y):
        matrixTranslate = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])

    def Scalation(sx, sy):
        matrixScalation = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def Rotation(theta):
        matrixRotation = np.array([[math.cos(math.radians(theta)), -math.sin(math.radians(theta)), 0], [math.sin(math.radians(theta)), math.cos(math.radians(theta)), 0], [0, 0, 1]])

    def Shear(shx, shy):
        matrixShear = np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]])

    def Reflection():
        matrixReflection = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]) 