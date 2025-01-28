
import fiona
import numpy as np
from scipy.spatial import distance,Voronoi
from shapely.geometry import Polygon,LineString,Point
import geopandas as geo
import matplotlib.pyplot as plt
from pyInegi.generalizacion import webMap
from pyInegi.basico import funciones as func


def chaikin_smooth(coords, refinements=5):
    for _ in range(refinements):
        new_coords = []
        for i in range(len(coords) - 1):
            p0 = coords[i]
            p1 = coords[i + 1]
            new_coords.append((0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1]))
            new_coords.append((0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1]))
        coords = new_coords
    return coords




def linea_central_distancia(puntos,pun):
    puntos = np.array(puntos)
    distancias = distance.cdist(puntos, np.array(pun[:1]))
    distancias_minimas = np.zeros(len(puntos))
    for i in range(len(puntos)):
        distancias_minimas[i] = np.min(distancias[i])
        #distancias_minimas[i] = np.min(distancias[i, np.arange(len(puntos)) != i])
    puntos_con_distancias = np.column_stack((puntos, distancias_minimas))
    puntos_ordenados = puntos_con_distancias[puntos_con_distancias[:, 2].argsort()]
    
    return puntos_ordenados[:, :2]

def xy(c):
    return [geo[0] for geo in c],[geo[1] for geo in c]

def shpTmp(gdf,nom):
    gdf.to_file(nom)
    return nom


dat = geo.read_file("DatosEntrada/costa-acapulco.shp",rows=100)
CRS = dat.crs.to_string()
print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*  DIR(GEOM)  *-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
datos,tipos,names,color=[],[],[],[]
for id,row in dat.iloc[10:15].iterrows():
    geom = row.geometry
    geom = geom.segmentize(5)
    puntos=list(geom.exterior.coords)
    for interior in geom.interiors:
        puntos.extend(list(interior.coords))
    v1 = Voronoi(np.array(puntos))
    v2 = geo.GeoDataFrame(geometry=[geom],crs=CRS)
    print("*--*-*-*-*-**-*-*-*-***  v2  ***-*-*-*-*-*-*-*-**-*-*-")

    v2v = v2.voronoi_polygons()
    print("*--*-*-*-*-**-*-*-*-***  v2v   ***-*-*-*-*-*-*-*-**-*-*-")

    vtx_in = [v for v in v1.vertices if Point(v).intersects(geom) ]
    #v1_df = geo.GeoDataFrame(data=[{"id":id} for id in range(len(v1.vertices))],geometry=[Point(*v) for v in v1.vertices],crs=CRS)
    v1_df = geo.GeoDataFrame(data=[{"id":i} for i in range(1,len(vtx_in)+1)],geometry=[Point(*v) for  v in vtx_in],crs=CRS)
    voro2 = Polygon(v1_df.geometry)
    voro2_df = geo.GeoDataFrame(geometry=[voro2],crs=CRS)
    voro_poly=voro2_df.voronoi_polygons()
    voro_poly.to_file(func.renombrar("DatosSalida/voro2.shp"))
    #v1_df.set_index("id")
    #vv = geo.GeoDataFrame(geometry=[Point(*p) for p in vtx_in],crs=CRS)
    #v2 = voronoi_polygons(tmp)
    pntOrd = linea_central_distancia(vtx_in,puntos)

    df = geo.GeoSeries([LineString(chaikin_smooth(list(pntOrd[::-1]),15))])
    punt_df = geo.GeoDataFrame(data=[{"OID":i} for i in range(1,len(pntOrd)+1)],geometry=[Point(*p) for p  in pntOrd[::-1]], crs=CRS)
    
    tempo = geo.GeoDataFrame(geometry=df,crs=CRS)
    print(tempo)

    simpli = tempo.simplify(tolerance=10)
    df.to_file("DatosSalida/LineaCentral.shp")
    simpli.to_file("DatosSalida/LineaCentral_Simplifficada.shp")
    punt_df.to_file("DatosSalida/PuntosOrdenados.shp")
    print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* {id} *-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

    print(type(v1_df))
    nom = f"DatosSalida/v1_.shp"
    v1_df.to_file(nom)
    datos.append(nom)
    tipos.append("POINT")
    names.append(nom)
    color.append("red")
    
    print(type(v2))
    nom = f"DatosSalida/v2_.shp"
    v2.to_file(nom)
    datos.append(nom)
    tipos.append("POLYGON")
    names.append(nom)
    color.append("blue")
    
    print(type(v2v))
    nom = f"DatosSalida/v2v.shp"
    v2v.to_file(nom)
    datos.append(nom)
    tipos.append("POLYGON")
    names.append(nom)
    color.append("green")

webMap.WebMAP(datos=datos,tipos=tipos,names=names,color=color)


    #pol = tmp.explore(name=f"Poligono {poligono[0]}", color="gray",edgecolor="blue",popup=True)
    #vtx = v1_df.explore(m=pol,name=f"Vertices pol-{poligono[0]}",color="red",markersize=10,popup=True)
    #mapa = punt_df.explore(m=mapa, name = f"Ordenados {poligono[0]}",color="green",markersize=1,popup=True)
    #folium.TileLayer("OpenStreetMap").add_to(mapa)
    #folium.LayerControl().add_to(mapa)
    #mapa.show_in_browser()             4492018988