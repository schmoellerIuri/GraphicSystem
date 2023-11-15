import numpy as np
import math

class Object:
    def __init__(self, name, listVertex):
        self.name = name
        self.listVertex = listVertex

    def GetMatrizTranslacao(x, y):
        return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])

    def GetMatrizEscala(sx, sy):
        return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def GetMatrizRotacao(theta):
        return np.array([[math.cos(math.radians(theta)), -math.sin(math.radians(theta)), 0], [math.sin(math.radians(theta)), math.cos(math.radians(theta)), 0], [0, 0, 1]])

    def GetMatrizCisalhamento(shx, shy):
        return np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]])

    def GetMatrizReflexao():
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]) 