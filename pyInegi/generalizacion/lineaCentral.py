import os
from time import time as t
import folium
import geopandas
import numpy as np
from multiprocessing import Pool, freeze_support
import json
import argparse
from shapely import LineString
from pyInegi.shapely_tools3 import intersection_points
import matplotlib.pyplot as plt


def renombrar(name):
	noms = name.split(".")
	if not os.path.exists(name): 
		return name
	newName = (noms[0][:-1] + str(int(noms[0][-1]) + 1) if noms[0][-1].isdigit() else f"{noms[0]}_1")
	nomComp = f"{newName}.{noms[1]}"
	return renombrar(nomComp)


def enParalelo(polOrig):
	from variables import parametros as p, CRS
	ini=t()
	idPol = polOrig[0]
	print(f"[PID: {os.getpid()}] Poligono: {idPol}...")
	geomOrig = polOrig[1]["geometry"]
	geomOrig = geomOrig.buffer(0)
	segm = geomOrig.segmentize(p['dist'])
	df_segm = geopandas.GeoDataFrame(geometry=[segm],crs=CRS)
	voroPoly = df_segm.voronoi_polygons()
	borde = segm.boundary
	DFclip=voroPoly.boundary.clip(geomOrig)
	union = DFclip.union_all()
	sept = list(union.geoms) 
	DFclip=geopandas.GeoDataFrame(data=[{"id":i} for i in range(1,len(sept)+1)], geometry=sept)
	DFclip.set_index('id',inplace=True)
	b = intersection_points(DFclip.index,DFclip.values,borde,1)
	centrales = DFclip.drop(index=b)
	union = centrales.union_all()
	u = geopandas.GeoSeries([union])
	unir = u.line_merge()
	tempo = geopandas.GeoDataFrame(geometry=unir,crs=CRS)
	_geoms = tempo.simplify(tolerance=p['dist']*0.51)
	print("...Pol: %d  ->  Tiempo: %.3f seg." % (idPol,float(t()-ini)))
	return _geoms.values


def inicio(**a):
	print(" OBTENIENDO LINEAS CENTRALES.... ")
	print(f"parametros: {json.dumps(a,indent=4)}")
	t1=t()
	orig =  geopandas.read_file(a["file"],rows=None if a["rows"]==-1 else a["rows"], columns=["geometry"])
	indice=orig.sindex
	CRS = orig.crs.to_string()
	with open("variables.py", "w") as _var:
		_var.write(f"parametros = {json.dumps(a)} \n")
		_var.write(f"CRS='{CRS}'")
	_ge=[]
	with Pool(a["cpu"]) as pool:
		temp = pool.map(enParalelo,orig.iterrows())
		for tt in temp:
			_ge+=tt
		arr = np.asarray(_ge)
		voroDF = geopandas.GeoDataFrame(geometry=arr,crs=CRS)
		bordeTot = orig.boundary
		if not os.path.exists("DatosSalida"):
			os.mkdir("DatosSalida")
		bordeTot.to_file(renombrar("DatosSalida/borde.shp"))	
		result = renombrar("DatosSalida/lineaCentral.shp")
		voroDF.to_file(result)
	print("TIEMPO TOTAL: %.3f " % float(t()-t1))
	print(f"Las líneas Centrales resultantes se encuentran en la siguiente ruta: {os.getcwd().replace("\\","/")}/{result}")
	if a["web"]==1:
		m0 = bordeTot.explore(name="Poligonos Exteriores",color="red")
		m1 = voroDF.explore(m=m0,name="Lineas Centrales",color="black", tooltip=True)
		folium.TileLayer("OpenStreetMap",show=True).add_to(m1)
		folium.LayerControl().add_to(m1)
		m1.show_in_browser()
    


if __name__ == "__main__":
	freeze_support()
	args = argparse.ArgumentParser(description="Regresa  las lineas centrales de cualquier poligono en formato shape")
	args.add_argument("file",type=str,help="Ruta de la capa de poligonos")
	args.add_argument("dist",type=int,nargs="?",default=10,help="Longitud maxima de las lineas al segmentar los poligonos. DEFAULT 10m")
	args.add_argument("cpu",type=int,nargs="?",default=os.cpu_count(),help=f"Cantidad de nucleos del procesador a utilizar de forma paralela. DEFAULT {os.cpu_count()} CPUs para  este equipo")
	args.add_argument("web",type=int,nargs="?",default=0,help="Muestra el resultado en un sistema de información geográfica Web. DEFAULT 0 (Falso, No)")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	args = args.parse_args()
	inicio(args)        

        
# import pyInegi

# f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
# f.run(gdb='MOPIGMA.gdb', feat='prueba2', camp=["*"],dist=15,ver=1)
