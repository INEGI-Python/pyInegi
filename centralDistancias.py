
import numpy as np
from scipy.spatial import distance,Voronoi
import matplotlib.pyplot as plt

from shapely import Polygon


def linea_central_distancia(puntos):
    puntos = np.array(puntos)
    distancias = distance.cdist(puntos, puntos)
    distancias_minimas = np.zeros(len(puntos))
    for i in range(len(puntos)):
        distancias_minimas[i] = np.min(distancias[i, np.arange(len(puntos)) != i])
    puntos_con_distancias = np.column_stack((puntos, distancias_minimas))
    puntos_ordenados = puntos_con_distancias[puntos_con_distancias[:, 2].argsort()]
    return puntos_ordenados[:, :2]

def xy(c):
    return [geo[0] for geo in c],[geo[1] for geo in c]

# Ejemplo de uso:
coor = ((0, 0),(2,-1),(4,3) ,(5, 5), (0, 6), (-4,5),(-5,3), (-3, 1),(0,0))
poly = Polygon(coor)
print(poly)
voro = Voronoi(np.array(coor))

print(voro.vertices)
print(voro.ridge_vertices)



plt.plot(*xy(coor))
plt.plot(*xy(voro.vertices))

