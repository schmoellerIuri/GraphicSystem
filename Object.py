import numpy as np
import math
from matplotlib.patches import Polygon

class Object:
    def __init__(self, name, listVertex, listScatter, color='cyan'):
        self.name = name
        self.listVertex = listVertex    
        self.polygon = Polygon(listVertex, closed=True, edgecolor='blue', facecolor=color, alpha=0.5)
        self.listScatter = listScatter
        self.SetPatch(self.polygon)
        self.FindCentroid()

    def Undraw(self):
        self.patch.remove()
        for scatter in self.listScatter:
            scatter.remove()

    def SetPatch(self, patch):
        self.patch = patch

    def FindCentroid(self):
        coordsX = [vertex[0] for vertex in self.listVertex]
        coordsY = [vertex[1] for vertex in self.listVertex]
        self.centroidX = np.mean(coordsX)
        self.centroidY = np.mean(coordsY)

    def ApplyTransformationMatrix(self, matrix):
        for i in range(len(self.listVertex)):
            point = np.array([self.listVertex[i][0], self.listVertex[i][1], 1])
            transformed_point = np.dot(matrix, point)
            self.listVertex[i] = (transformed_point[0], transformed_point[1])
        self.polygon.set_xy(self.listVertex)
        self.FindCentroid()

    def Translate(self, x, y):
        matrixTranslate = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])
        self.ApplyTransformationMatrix(matrixTranslate)

    def Scale(self, sx, sy):
        matrixScale = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        Translate(-self.centroidX, -self.centroidY)
        self.ApplyTransformationMatrix(matrixScale)

    def Rotate(self, theta):
        matrixRotation = np.array([[math.cos(math.radians(theta)), -math.sin(math.radians(theta)), 0],
                                   [math.sin(math.radians(theta)), math.cos(math.radians(theta)), 0],
                                   [0, 0, 1]])
        Translate(-self.centroidX, -self.centroidY)
        self.ApplyTransformationMatrix(matrixRotation)

    def Shear(self, shx, shy):
        matrixShear = np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]])
        Translate(-self.centroidX, -self.centroidY)
        self.ApplyTransformationMatrix(matrixShear)

    def Reflect(self, sense):
        if sense == "Horizontal":
            matrixReflection = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
        elif sense == "Vertical":
            matrixReflection = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        Translate(-self.centroidX, -self.centroidY)
        self.ApplyTransformationMatrix(matrixReflection)
