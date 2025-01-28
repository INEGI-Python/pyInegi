
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

def simplificarLinea(coords,dist):
    coords = np.array(coords)
    new_coords=[coords[0]]
    for i in range(1,len(coords)-1):
        b = coords[i]
        a_b = func.dist2pnts(new_coords[-1][0],new_coords[-1][1],b[0],b[1])
        if a_b>dist:
            new_coords.append(b)
    new_coords.append(coords[-1])
    return new_coords
    


def linea_central_distancia(puntos,pun):
    puntos = np.array(puntos)
    distancias = distance.cdist(puntos, np.array([pun]))
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


dat = geo.read_file("DatosEntrada/SinIslas.shp",rows=300)
CRS = dat.crs.to_string()
datos,tipos,names,color=[],[],[],[]
layers = [[],[],[],[],[]]
for id,row in dat.iterrows():
    geom = row.geometry
    segm = geom.buffer(0).segmentize(8)
    puntos=list(segm.exterior.coords)
    for interior in segm.interiors:
        puntos.extend(list(interior.coords))
    v1 = Voronoi(np.array(puntos))
    #v2 = geo.GeoDataFrame(geometry=[geom],crs=CRS)
    vtx_in = [v for v in v1.vertices if Point(v).intersects(geom) ]
    v1_df = geo.GeoDataFrame(data=[{"id":i} for i in range(1,len(vtx_in)+1)],geometry=[Point(*v) for  v in vtx_in],crs=CRS)
   
    
    if len(vtx_in)>1:
        pntOrd = linea_central_distancia(vtx_in,puntos[0])[::-1]

        df = geo.GeoSeries([LineString(pntOrd)],crs=CRS)
        layers[0].append(LineString(pntOrd),)
        punt_df = geo.GeoDataFrame(geometry=[Point(*p) for p  in pntOrd], crs=CRS)
        [layers[3].append(Point(*p)) for p  in pntOrd]
        simpli = geo.GeoDataFrame(geometry=[LineString(simplificarLinea(pntOrd,16))],crs=CRS)
        #simpli = tempo.union_all().simplify(5)
        layers[1].append(LineString(simpli.__geo_interface__['features'][0]['geometry']['coordinates']))
        #smooth = geo.GeoSeries([LineString(chaikin_smooth(simpli.geometry[0].coords,5))],crs=CRS)
        layers[2].append(LineString(chaikin_smooth(list(simpli.__geo_interface__['features'][0]['geometry']['coordinates']),5)))
        layers[4].append(segm)
        print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* {id} *-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        

linCen = geo.GeoDataFrame(geometry=layers[0],crs=CRS)
linSimpli = geo.GeoDataFrame(geometry=layers[1],crs=CRS)
linSuavi = geo.GeoDataFrame(geometry=layers[2],crs=CRS)
vertex = geo.GeoDataFrame(geometry=layers[3],crs=CRS)
pols = geo.GeoDataFrame(geometry=layers[4],crs=CRS)



capas=[{'GDF':"linSimpli",'nom':"LineaCentral_Simplifficada",'tipo':"LINESTRING",'color':"black"},{'GDF':"linCen",'nom':"LineaCentral",'tipo':"LINESTRING",'color':"red"},
       {'GDF':"linSuavi",'nom':"LineaCentral_Suavizada",'tipo':"LINESTRING",'color':"green"} ,{'GDF':"vertex",'nom':"PuntosOrdenados",'tipo':"POINT",'color':"blue"},
       {'GDF':"pols",'nom':"Poligonos",'tipo':"POLYGON",'color':"gray"}]

for c in capas:
    nom = func.renombrar(f"DatosSalida/{c['nom']}.shp")
    eval(f"{c['GDF']}.to_file('{nom}')")
    datos.append(nom)
    tipos.append(c['tipo'])
    names.append(nom.split("/")[1])
    color.append(c['color'])

webMap.WebMAP(datos=datos,tipos=tipos,names=names,color=color)


    #pol = tmp.explore(name=f"Poligono {poligono[0]}", color="gray",edgecolor="blue",popup=True)
    #vtx = v1_df.explore(m=pol,name=f"Vertices pol-{poligono[0]}",color="red",markersize=10,popup=True)
    #mapa = punt_df.explore(m=mapa, name = f"Ordenados {poligono[0]}",color="green",markersize=1,popup=True)
    #folium.TileLayer("OpenStreetMap").add_to(mapa)
    #folium.LayerControl().add_to(mapa)
    #mapa.show_in_browser()             4492018988