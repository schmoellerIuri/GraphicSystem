import numpy as np
import math
from matplotlib.patches import Polygon

class Object:
    def __init__(self, name, listVertex, listScatter, color='cyan'):
        self.name = name
        self.listVertex = listVertex 
        self.color = color   
        self.polygon = Polygon(listVertex, closed=True, edgecolor='blue', facecolor=color, alpha=0.5)
        self.listScatter = listScatter
        self.FindCentroid()

    def Undraw(self):
        self.patch.remove()
        for scatter in self.listScatter:
            scatter.remove()

    def SetPatch(self, patch):
        self.patch = patch

    def GetMatrizTranslacao(self, x, y):
        return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])

    def GetMatrizEscala(self, sx, sy):
        return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def GetMatrizRotacao(self, theta):
        return np.array([[math.cos(math.radians(theta)), -math.sin(math.radians(theta)), 0], [math.sin(math.radians(theta)), math.cos(math.radians(theta)), 0], [0, 0, 1]])

    def GetMatrizCisalhamento(self, shx, shy):
        return np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]])

    def GetMatrizReflexao(self, sense):
        if sense == "Horizontal":
            return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
        elif sense == "Vertical":
            return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

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
        self.polygon = Polygon(self.listVertex, closed=True, edgecolor='blue', facecolor=self.color, alpha=0.5)

    def Translate(self, x, y):
        matrixTranslate = self.GetMatrizTranslacao(x, y)
        self.ApplyTransformationMatrix(matrixTranslate)

    def Scale(self, sx, sy):
        matrixes = []
        matrixes.append(self.GetMatrizTranslacao(-self.centroidX, -self.centroidY))
        matrixes.append(self.GetMatrizEscala(sx, sy))
        matrixes.append(self.GetMatrizTranslacao(self.centroidX, self.centroidY))
        matrixConcatenated = self.GetConcatenatedMatrix(matrixes)
        self.ApplyTransformationMatrix(matrixConcatenated)
        self.FindCentroid()

    def Rotate(self, theta):
        matrixes = []
        matrixes.append(self.GetMatrizTranslacao(-self.centroidX, -self.centroidY))
        matrixes.append(self.GetMatrizRotacao(theta))
        matrixes.append(self.GetMatrizTranslacao(self.centroidX, self.centroidY))
        matrixConcatenated = self.GetConcatenatedMatrix(matrixes)
        self.ApplyTransformationMatrix(matrixConcatenated)
        self.FindCentroid()

    def Shear(self, shx, shy):
        matrixes = []
        matrixes.append(self.GetMatrizTranslacao(-self.centroidX, -self.centroidY))
        matrixes.append(self.GetMatrizCisalhamento(shx, shy))
        matrixes.append(self.GetMatrizTranslacao(self.centroidX, self.centroidY))
        matrixConcatenated = self.GetConcatenatedMatrix(matrixes)
        self.ApplyTransformationMatrix(matrixConcatenated)
        self.FindCentroid()

    def Reflect(self, sense):
        matrixes = []
        matrixes.append(self.GetMatrizTranslacao(-self.centroidX, -self.centroidY))
        matrixes.append(self.GetMatrizReflexao(sense))
        matrixes.append(self.GetMatrizTranslacao(self.centroidX, self.centroidY))
        matrixConcatenated = self.GetConcatenatedMatrix(matrixes)
        self.ApplyTransformationMatrix(matrixConcatenated)
        self.FindCentroid()

    def GetConcatenatedMatrix(self, matrixes):
        concatenatedMatrix = np.identity(3)
        matrixes.reverse()

        for matrix in matrixes:
            concatenatedMatrix = np.dot(concatenatedMatrix, matrix)
        return concatenatedMatrix
