
import numpy as np
from scipy.spatial import distance,Voronoi
from shapely.geometry import Polygon,LineString,Point
import geopandas as geo
import matplotlib.pyplot as plt
from pyInegi.generalizacion import webMap
from pyInegi.basico import funciones as func
from multiprocessing import Pool
import os,argparse,json
from time import time as t


def variables(a):
    ruta=os.getcwd()
    print(ruta)
    with open(f"variables.py", "w") as _var:
        _var.write(f"parametros = {json.dumps(a)} \n")
        _var.write(f"cont = [] \n")
        _var.write("def contar(n):\n")
        _var.write("\tcont.append(n)\n")
        _var.close()

def suavecito(coords, refinements=5):
    for _ in range(refinements):
        new_coords = [coords[0]]
        for i in range(len(coords) - 1):
            p0 = coords[i]
            p1 = coords[i + 1]
            new_coords.extend(
                (
                    (0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1]),
                    (0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1]),
                )
            )
        new_coords.append(coords[-1])
        coords = new_coords
    return coords

def simplecito(coords,dist):
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
    #puntos = np.array(puntos)
    distancias = distance.cdist(puntos, np.array([pun]))
    distancias_minimas = np.zeros(len(puntos))
    for i in range(len(puntos)):
        distancias_minimas[i] = np.min(distancias[i])
    puntos_con_distancias = np.column_stack((puntos, distancias_minimas))
    puntos_ordenados = puntos_con_distancias[puntos_con_distancias[:, 2].argsort()]    
    return puntos_ordenados[:, :2]


def enParalelo(row):
    from variables import contar
    contar(1)
    from variables import parametros as p, cont  
    layers = []
    geom = row[1].geometry
    segm = geom.buffer(0).segmentize(p['dist'])
    puntos=list(segm.exterior.coords)
    if len(cont)%100==0:
        func.imp(f" Procesando poligono {row[0]} - PID: {os.getpid()}")
    if len(segm.interiors)>0:
        return []
    try:
        v1 = Voronoi(np.array(puntos))
        vtx_in = [v for v in v1.vertices if Point(v).intersects(geom) ]
    except Exception as e:
        return []
    
    if len(vtx_in)>1:
        fact=2
        pntOrd = linea_central_distancia(np.array(vtx_in),puntos[0])[::-1]
        linea = LineString(pntOrd)
        while not linea.is_simple:
            pos = int(len(puntos)/fact)
            pntOrd = linea_central_distancia(np.array(vtx_in),puntos[pos])[::-1]
            linea = LineString(pntOrd)
            fact += 1
            if fact>4:
                return []
        layers.append(LineString(pntOrd))
        #punt_df = geo.GeoDataFrame(geometry=[Point(*p) for p  in pntOrd], crs=p['CRS'])
        simpli = geo.GeoDataFrame(geometry=[LineString(simplecito(pntOrd,p['simp']))],crs=p['CRS'])
        layers.append(LineString(simpli.__geo_interface__['features'][0]['geometry']['coordinates']))
        layers.append(LineString(simplecito(suavecito(list(simpli.__geo_interface__['features'][0]['geometry']['coordinates']),p['suavi']),p['simp'])))
        layers.append(segm)
        layers.append([Point(*p) for p  in pntOrd])
    
    return layers



def LineaCentral_SinHuecos(**a):
    ini=t()
    dat = geo.read_file(a['file'],rows=None if a["rows"]==-1 else a["rows"])
    CRS = dat.crs.to_string()
    a['CRS']=CRS
    a['cantPol']=dat.index.stop
    variables(a)
    with Pool(a['cpu']) as pool:
        resp = pool.map(enParalelo,dat.iterrows())
        vecLinCen,vecSimpli,vecSuavi=[],[],[]
        for r in resp:
            if len(r)>0:
                vecLinCen.append(r[0])
                vecSimpli.append(r[1])
                vecSuavi.append(r[2])

        linCen = geo.GeoDataFrame(geometry=vecLinCen,crs=CRS)     
        linSimpli = geo.GeoDataFrame(geometry=vecSimpli,crs=CRS)  
        linSuavi = geo.GeoDataFrame(geometry=vecSuavi,crs=CRS)   
    
        print(f"Poligonos procesados -->  {a['cantPol']}   Tiempo: {t()-ini} seg.")
        if not os.path.exists("DatosSalida"):
            os.mkdir("DatosSalida")
        if a['web']==1:
            capas=[{'GDF':"linSimpli",'nom':"LineaCentral_Simplifficada",'tipo':"LINESTRING",'color':"black"},{'GDF':"linCen",'nom':"LineaCentral",'tipo':"LINESTRING",'color':"red"},{'GDF':"linSuavi",'nom':"LineaCentral_Suavizada",'tipo':"LINESTRING",'color':"green"}] 
            datos,tipos,names,color=[],[],[],[]
            for c in capas:
                nom = func.renombrar(f"DatosSalida/{c['nom']}.shp")
                eval(f"{c['GDF']}.to_file('{nom}')")
                datos.append(nom)
                tipos.append(c['tipo'])
                names.append(nom.split("/")[1])
                color.append(c['color'])
            webMap.WebMAP(datos=datos,tipos=tipos,names=names,color=color)
        else:
            linSuavi.to_file(func.renombrar(f"DatosSalida/LineasCentralSuavizada.shp"))



if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Regresa  las líneas centrales de poligons largos y sin huecos")
	args.add_argument("file",type=str,help="Ruta de la capa de polígonos")
	args.add_argument("dist",type=int,nargs="?",default=10,help="Longitud máxima de las líneas al segmentar los polígonos. DEFAULT 10 m")
	args.add_argument("simp",type=int,nargs="?",default=12,help="Longitud minima de vertice a vertice despues del simplificadp. DEFAULT 12 m")
	args.add_argument("suavi",type=int,nargs="?",default=5,help="Grado de suavizado. DEFAULT 5 ")
	args.add_argument("cpu",type=int,nargs="?",default=os.cpu_count(),help=f"Cantidad de nucleos del procesador a utilizar de forma paralela. DEFAULT {os.cpu_count()} CPUs para  este equipo")
	args.add_argument("web",type=int,nargs="?",default=0,help="Muestra el resultado en un sistema de información geográfica Web. DEFAULT 0")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	argumentos = args.parse_args()
	print(argumentos)
	LineaCentral_SinHuecos(argumentos)