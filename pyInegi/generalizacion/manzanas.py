import sys,os
import numpy as np
import argparse
import geopandas as geo
import matplotlib
matplotlib.use("TkAgg") 
import matplotlib.pyplot as plt
from time import time as t
from shapely.ops import unary_union,polygonize




def shp(dat,nom):
    dat.to_file(f"DatosSalida/{nom}", driver="ESRI Shapefile")

def remove_colinear_points(geom, tolerance=5):
		if geom.geom_type == "Polygon":
			coords = list(geom.exterior.coords)
			new_coords = [coords[0]]
			for i in range(1, len(coords) - 1):
				p0 = np.array(new_coords[-1])
				p1 = np.array(coords[i])
				p2 = np.array(coords[i + 1])
				v1 = p1 - p0
				v2 = p2 - p1
				cross = np.cross(v1, v2)
				if np.abs(cross) > tolerance:
					new_coords.append(coords[i])
			new_coords.append(coords[-1])
			return type(geom)(new_coords)
		return geom

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
	if fuente[-1].split(".")[-1] not in ["shp","gpkg","geojson"]:
		if fuente[-2].split(".")[-1] == "gdb":
			gdf = geo.read_file(a.file[0:len(a.file)-len(fuente[-1])],layer=fuente[-1],rows=None if a.rows == -1 else a.rows)
		else:
			raise ValueError("El archivo debe ser un shapefile, geopackage,geojson o feature class dentro de un geodatabase")
	else:
		gdf = geo.read_file(a.file,rows=None if a.rows == -1 else a.rows)	
	print("Elimina ángulos colineales de las geometrías de la capa a procesar...")
	gdf["geometry"] = gdf["geometry"].apply(remove_colinear_points)
	os.mkdir("DatosSalida") if not os.path.exists("DatosSalida") else None
	shp(gdf,"manzanas_sin_colineales.shp")
	poligonos = [generaTriangulos_lineasFuera(gdf.loc[i,"geometry"],a.dist,gdf.crs,i) for i in gdf.head().index]
	print("Proceso finalizado. Tiempo: %.3f seg" % (t()-ini))
	print("Mostrando resultados...")
	poligonos_gdf = geo.GeoDataFrame(geometry=[poly for sublist in poligonos for poly in sublist], crs=gdf.crs)
	shp(poligonos_gdf,"manzanas_sin_privadas.shp")
	poligonos_gdf.plot(facecolor="none",edgecolor="blue")
	plt.title("Manzanas sin privadas ni áreas comunes")
	gdf.plot(facecolor="none",edgecolor="red")
	plt.title("Manzanas originales")
	plt.show()

if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Generaliza manzanas con privadas y áreas comunes")
	args.add_argument("file",type=str,help="Ruta de la capa de manzanas")
	args.add_argument("dist",type=int,nargs="?",default=10,help="Ancho máximo en metros de la privada a quitar. DEFAULT 10 m")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	args = args.parse_args()
	quitaPrivadas(args)        