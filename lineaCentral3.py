import os
from time import time as t
import folium
import geopandas
import numpy as np
from multiprocessing import Pool
import json
import argparse

from shapely import LineString, linestrings
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
	#print(DFclip.value_counts())
	union = DFclip.union_all()
	sept = list(union.geoms) 
	DFclip=geopandas.GeoDataFrame(data=[{"id":i} for i in range(1,len(sept)+1)], geometry=sept)
	#print(DFclip)
	DFclip.set_index('id',inplace=True)
	a,b = intersection_points(DFclip.index,DFclip.values,borde,0.1)
	centrales = DFclip.drop(index=b)
	union = centrales.union_all()
	u = geopandas.GeoSeries([union])
	unir = u.line_merge()
	tempo = geopandas.GeoDataFrame(geometry=unir,crs=CRS)
	#pegar = tempo.line_merge()
	_geoms = tempo.simplify(tolerance=p['dist']*0.51)
	print("...Pol: %d  ->  Tiempo: %.3f seg." % (idPol,float(t()-ini)))
	return _geoms.values


def inicio(a):
	t1=t()
	orig =  geopandas.read_file(a.file,rows=None if a.rows==-1 else a.rows)
	orig.set_index("OBJECTID",inplace=True)
	indice=orig.sindex
	CRS = orig.crs.to_string()
	with open("variables.py", "w") as _var:
		_var.write(f"parametros = {json.dumps({'file':a.file,'dist':a.dist,'rows':a.rows})} \n")
		_var.write(f"CRS='{CRS}'")
	_ge=[]
	with Pool() as pool:
		temp = pool.map(enParalelo,orig.iterrows())
		print(type(temp))
		for tt in temp:
			_ge+=tt
		arr = np.asarray(_ge)
		voroDF = geopandas.GeoDataFrame(geometry=arr,crs=CRS)
		#bordeTot = orig.boundary
		#bordeTot.to_file(renombrar("DatosSalida/borde.shp"))
		voroDF.to_file(renombrar("DatosSalida/lineaCentral.shp"))
		#voroDF.plot()
		#plt.show()
	print("TIEMPO TOTAL: %.3f " % float(t()-t1))




	#df_union = df_union.groupby('OBJECTID')['geometry'].agg(lambda x: union_all(x.values))
	#df_union = geopandas.GeoDataFrame(df_union, crs=CRS)
	#pegar=df_union.line_merge()
	#df_union['geometry'] = pegar.simplify(tolerance=a.dist*0.51)

	#puntosInter = geopandas.GeoDataFrame(geometry=inter,crs=CRS)
	#puntosInter.to_file(renombrar("DatosSalida/Intersecciones.shp"))
	
	print(f"TIEMPO TOTAL: {float(t()-t1)}")
	
	#m = puntosInter.explore(name="PuntosInter",color="blue",tooltip=True)
	#m0 = borde.explore(name="Poligonos Exteriores",color="red")
	#m1 = df_union.explore(m=m0,name="Voronoi Central",color="black", tooltip=True)
	#folium.TileLayer("OpenStreetMap",show=True).add_to(m1)
	#folium.LayerControl().add_to(m1)
	#m1.show_in_browser()
    

#class argumentos:
#	def __init__(self,f,r,d):
#		self.file=f
#		self.rows=r
#		self.dist=d
#args = argumentos("prueba3.shp",3,5)
#inicio(args)

if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Regresa  las lineas centrales de cualquier poligono")
    args.add_argument("file",type=str,help="Ruta de la capa de poligonos")
    args.add_argument("dist",type=int,nargs="?",default=10,help="Longitud maxima de las lineas al segmentar")
    args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. Default todos")
    args = args.parse_args()
    inicio(args)        

        
# import pyInegi

# f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
# f.run(gdb='MOPIGMA.gdb', feat='prueba2', camp=["*"],dist=15,ver=1)