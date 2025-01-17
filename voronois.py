
import folium
import numpy as np
from pyparsing import line
from scipy.spatial import distance,Voronoi
from shapely.geometry import Polygon,LineString,Point
import geopandas as geo
import matplotlib.pyplot as plt




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


dat = geo.read_file("DatosEntrada/SinIslas.shp",rows=1)
CRS = dat.crs.to_string()
dat.set_index("ORIG_FID")
print(dat.loc[0:,"geometry"])
puntos = []
for geom in dat.geometry:
    puntos.extend(list(geom.exterior.coords))
    for interior in geom.interiors:
        puntos.extend(list(interior.coords))
v1 = Voronoi(np.array(puntos))
v1_df = geo.GeoDataFrame(geometry=[Point(*v) for v in v1.vertices],crs=CRS)
print(v1.vertices)
pntOrd = linea_central_distancia(v1.vertices)
df = geo.GeoDataFrame(geometry=[LineString(pntOrd)], crs=CRS)
df.plot()

v2 = dat.voronoi_polygons()



#v1_df.to_file("DatosSalida/voroVerticesCosta.shp")
#v2.to_file("DatosSalida/voronoi_polygonCosta.shp")

