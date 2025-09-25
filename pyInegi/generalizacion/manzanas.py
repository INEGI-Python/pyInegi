



import argparse
import numpy as np
from turtle import pu
import geopandas as geo
import matplotlib
import shapely
matplotlib.use("TkAgg") 
import matplotlib.pyplot as plt
from time import time as t
import alphashape


def quitaPrivadas(a):
	
	gdf = None
	fuente=a.file.split("/" or "\\")
	if fuente[-1].split(".")[-1] not in ["shp","gpkg","geojson"]:
		ini = t()
		if fuente[-2].split(".")[-1] == "gdb":
			gdf = geo.read_file(a.file[0:len(a.file)-len(fuente[-1])],layer=fuente[-1])
		else:
			raise ValueError("El archivo debe ser un shapefile, geopackage,geojson o feature class dentro de un geodatabase")
	else:
		gdf = geo.read_file(a.file)
	print("Leyendo capa...")
	puntos = gdf.extract_unique_points()
	for p in puntos.geometry:
		result=alphashape.alphashape(geo.GeoDataFrame(geometry=[p.__geo_interface__["coordinates"][0]],crs=gdf.crs),0.95)
		print(result)
		result = geo.GeoDataFrame(geometry=[result],crs=gdf.crs)
		result.plot()
		plt.title("Manzanas "+str(p.length))
		plt.show()
	



if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Generaliza manzanas con privadas y áreas comunes")
	args.add_argument("file",type=str,help="Ruta de la capa de manzanas")
	args.add_argument("dist",type=int,nargs="?",default=10,help="Ancho máximo en metros de la privada a quitar. DEFAULT 10 m")
	args.add_argument("web",type=int,nargs="?",default=0,help="Muestra el resultado en un sistema de información geográfica Web. DEFAULT 0 (Falso, No)")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	args = args.parse_args()
	quitaPrivadas(args)        