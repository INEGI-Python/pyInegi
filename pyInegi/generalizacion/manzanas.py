from operator import ge
import os
import argparse
import geopandas as geo
from time import time as t
from shapely.ops import unary_union,polygonize
from .puntosColineares import remove_colinear_points

def feat(gdb,feature,nom):
	feature.to_file(gdb,layer=nom, driver="OpenFileGDB")

def generaTriangulos_lineasFuera(geom,dist,crs,i):
	gdf=geo.GeoDataFrame(geometry= [geom],crs=crs)
	triangulos = gdf.delaunay_triangles(tolerance=0,only_edges=True)
	contorno = gdf.boundary
	triangulos_outside = triangulos[~triangulos.within(gdf.union_all())]
	gdf_outside = geo.GeoDataFrame(geometry=triangulos_outside, crs=gdf.crs)
	mask_not_within_contorno = ~gdf_outside.geometry.apply(lambda line: any(line.within(bound) for bound in contorno))
	mask_length_less_Xm = gdf_outside.geometry.length < dist
	filtered_lines = gdf_outside[mask_not_within_contorno & mask_length_less_Xm]
	all_lines = list(filtered_lines.geometry) + list(contorno)
	merged_lines = unary_union(all_lines)
	polygons = list(polygonize(merged_lines))
	polygons = [unary_union(polygons)]
	return polygons

def quitaPrivadas(a):
	gdf = None
	fuente=a.file.split("/" or "\\")
	print("Leyendo capa...")
	ini = t()
	if fuente[-2].split(".")[-1] != "gdb":
		raise ValueError("El archivo debe ser un feature class dentro de un geodatabase")

	gdb =a.file[0:len(a.file)-len(fuente[-1])-1]
	print(f"Geodatabase: {gdb}")
	gdf = geo.read_file(gdb,layer=fuente[-1],rows=a.rows if a.rows>0 else None)
	gdf["OBJECTID"] = gdf.index + 1
	gdf.set_index("OBJECTID",inplace=True)
	gdf.loc[:, "geometry"] = gdf.geometry.buffer(0)
	campos = [c for c in gdf.columns if c not in ["geometry","objectid"]]
	print("Elimina ángulos colineales de las geometrías de la capa a procesar...")
	gdf["geometry"] = gdf["geometry"].apply(remove_colinear_points)
	print("Generalizando polígonos...")
	poligonos = [generaTriangulos_lineasFuera(gdf.loc[i,"geometry"],a.dist,gdf.crs,i) for i in gdf.index]
	print("Proceso finalizado. Tiempo: %.3f seg" % (t()-ini))
	print(f"Guardando resultados en la geodatabase...")
	poligonos_gdf = geo.GeoDataFrame(geometry=[poly for sublist in poligonos for poly in sublist], crs=gdf.crs)
	for col in campos:
		poligonos_gdf[col] = None
	for idx, polys in enumerate(poligonos):
		for poly in polys:
			for col in campos:
				poligonos_gdf.loc[poligonos_gdf.geometry == poly, col] = gdf.iloc[idx][col]
	feat(gdb,poligonos_gdf,a.out)
	if a.prev==1:
		import matplotlib
		matplotlib.use("TkAgg") 
		import matplotlib.pyplot as plt
		poligonos_gdf.plot(facecolor="none",edgecolor="blue")
		plt.title("Poligonos procesados")
		gdf.plot(facecolor="none",edgecolor="red")
		plt.title("Poligonos originales")
		plt.show()



if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Generaliza poligonos quitando espacios que se adentran, como por ejemplo privadas en manzanas. ")
	args.add_argument("file",type=str,help="Ruta absoluta o relativa del feature class a procesar")
	args.add_argument("dist",type=int,help="Ancho máximo en metros del espacio a quitar.")
	args.add_argument("out",type=str, help="Nombre del feature class de salida.")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	args.add_argument("prev",type=int,nargs="?",default=0,help="Si es 1, muestra una vista previa de los poligonos procesados. DEFAULT 0")
	args = args.parse_args()
	quitaPrivadas(args)        



	# Ejemplo de uso por consola:
	# python manzanas.py "DatosEjemplo/urbana.gdb/mzas" 13 "manzanas_sin_privadas" 100 1	
	# Donde:
	# "DatosEjemplo/urbana.gdb/mzas" es la ruta al feature class de manzanas
	# 13 es la distancia máxima en metros de la privada a quitar
	# "manzanas_sin_privadas" es el nombre del feature class de salida
	# 100 es la cantidad de registros a usar (opcional)
	# 1 es el indicador para mostrar una vista previa (opcional)	