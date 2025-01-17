import os
from time import time as t
import folium
import geopandas
import numpy as np
from multiprocessing import Pool, freeze_support
import json
import argparse
from shapely import LineString
from shapely.geometry import GeometryCollection,MultiLineString
from ..basico.funciones import interseccion,renombrar
import matplotlib.pyplot as plt


def registrar(name,registro,pols={'cont':-1}):
	if pols['cont']==-1: return 0 
	with open(name,"+a") as reg:
		reg.write(f"{registro}")
		reg.close()
		#if pols['cont'] % int(pols['total']/10) == 0:
			#print(f"[{pols['cont']}]")
		return 1




def enParalelo(polOrig):
	from pyInegi.auxiliar.variables import parametros as p, CRS, Poligonos as pols
	ini=t()
	idPol = polOrig[0]
	geomOrig = polOrig[1]["geometry"]
	geomOrig = geomOrig.buffer(0)  
	segm = geomOrig.segmentize(p['dist'])
	df_segm = geopandas.GeoDataFrame(geometry=[segm],crs=CRS)
	voroPoly = df_segm.voronoi_polygons()
	borde = segm.buffer(p['dist']*-1).boundary
	DFclip=voroPoly.boundary.clip(geomOrig)
	union = DFclip.union_all()
	sept = list(union.geoms) 
	DFclip=geopandas.GeoDataFrame(data=[{"id":i} for i in range(1,len(sept)+1)], geometry=sept)
	DFclip.set_index('id',inplace=True)
	b = interseccion(DFclip.index,DFclip.values,borde,0.1,0.0)
	centrales = DFclip.drop(index=b)
	union = centrales.union_all()
	u = geopandas.GeoSeries([union])
	unir = u.line_merge()
	tempo = geopandas.GeoDataFrame(geometry=unir,crs=CRS)
	_geoms = tempo.simplify(tolerance=p['dist']*1.01)
	reg_pol = f"[{pols['cont']} de  {pols['total']}]  PID: {os.getpid()} --  ID Pol: {idPol} -- Tiempo: {float(t()-ini).__round__(3)} seg. \n"
	pols['cont'] += registrar("registros.log",reg_pol,pols)
	return _geoms.values


def LineaCentral(**a):
	log = open("registros.log","w")
	log.close()
	print(" OBTENIENDO LINEAS CENTRALES.... ")
	print(f"Parametros: {json.dumps(a,indent=4)}")
	print(f"\nCargando su archivo de datos, espere por favor....")
	t1=t()
	orig =  geopandas.read_file(a["file"],rows=None if a["rows"]==-1 else a["rows"], columns=["geometry"])
	indice=orig.sindex
	CRS = orig.crs.to_string()
	ruta=os.getcwd()
	with open(f"{ruta}/pyInegi/auxiliar/variables.py", "w") as _var:
		_var.write(f"parametros = {json.dumps(a)} \n")
		_var.write(f"CRS='{CRS}'\n")
		p = {'total':orig.index.stop,'cont':1}
		_var.write(f"Poligonos = {p}")
		_var.close() 
	_linCen = []
	with Pool(a["cpu"]) as pool:
		temp = pool.map(enParalelo,orig.iterrows())
		for tt in temp:
			_linCen+=tt
		arr = np.asarray(_linCen)
		voroDF = geopandas.GeoDataFrame(geometry=arr,crs=CRS)
		bordeTot = orig.buffer(a["dist"]*-2).boundary
		if not os.path.exists("DatosSalida"):
			os.mkdir("DatosSalida")
		bordeTot.to_file(renombrar("DatosSalida/borde.shp"))	
		result = renombrar(f"DatosSalida/lineaCentral_{a['dist']}m.shp") 
		#buff_DF.to_file("DatosSalida/buffer_-2m.shp")
		voroDF.to_file(result)
	time_tot = "TIEMPO TOTAL: %.3f " % float(t()-t1)
	print(time_tot)
	registrar("registros.log",time_tot)
	if a["web"]==1:
		m0 = bordeTot.explore(name="Poligonos Exteriores",color="red")
		m1 = voroDF.explore(m=m0,name="Lineas Centrales",color="black", tooltip=True)
		folium.TileLayer("OpenStreetMap",show=True).add_to(m1)
		folium.LayerControl().add_to(m1)
		m1.show_in_browser()
	return os.getcwd().replace("\\","/")+result
    

if __name__ == "__main__":
	freeze_support()
	args = argparse.ArgumentParser(description="Regresa  las líneas centrales de cualquier polígono en formato shape")
	args.add_argument("file",type=str,help="Ruta de la capa de polígonos")
	args.add_argument("dist",type=int,nargs="?",default=10,help="Longitud máxima de las líneas al segmentar los polígonos. DEFAULT 10 m")
	args.add_argument("cpu",type=int,nargs="?",default=os.cpu_count(),help=f"Cantidad de nucleos del procesador a utilizar de forma paralela. DEFAULT {os.cpu_count()} CPUs para  este equipo")
	args.add_argument("web",type=int,nargs="?",default=0,help="Muestra el resultado en un sistema de información geográfica Web. DEFAULT 0 (Falso, No)")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	args = args.parse_args()
	LineaCentral(args)        

        
# import pyInegi

# f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
# f.run(gdb='MOPIGMA.gdb', feat='prueba2', camp=["*"],dist=15,ver=1)
