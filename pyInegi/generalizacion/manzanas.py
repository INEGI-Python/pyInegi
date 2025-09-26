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
		print(geom.geom_type)
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
				print(np.abs(cross))
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
	gdf_polygons = geo.GeoDataFrame(geometry=polygons, crs=gdf.crs)
	shp(gdf_polygons,f"poligonoGenerado_{i}.shp")
	return gdf_polygons

def quitaPrivadas(a):
	gdf = None
	fuente=a.file.split("/" or "\\")
	print("Leyendo capa...")
	ini = t()
	if fuente[-1].split(".")[-1] not in ["shp","gpkg","geojson"]:
		if fuente[-2].split(".")[-1] == "gdb":
			gdf = geo.read_file(a.file[0:len(a.file)-len(fuente[-1])],layer=fuente[-1])
		else:
			raise ValueError("El archivo debe ser un shapefile, geopackage,geojson o feature class dentro de un geodatabase")
	else:
		gdf = geo.read_file(a.file)	
	# Elimina ángulos colineales de las geometrías en gdf
	gdf["geometry"] = gdf["geometry"].apply(remove_colinear_points)
	shp(gdf,"manzanas_sin_colineales.shp")

	for i in gdf.head(a.rows).index:
		generaTriangulos_lineasFuera(gdf.loc[i,"geometry"],a.dist,gdf.crs,i).plot()
		plt.title(f"Polígonos generados {i}")
	plt.show()
	print("Proceso finalizado. Tiempo: %.3f seg" % (t()-ini))

if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Generaliza manzanas con privadas y áreas comunes")
	args.add_argument("file",type=str,help="Ruta de la capa de manzanas")
	args.add_argument("dist",type=int,nargs="?",default=10,help="Ancho máximo en metros de la privada a quitar. DEFAULT 10 m")
	args.add_argument("web",type=int,nargs="?",default=0,help="Muestra el resultado en un sistema de información geográfica Web. DEFAULT 0 (Falso, No)")
	args.add_argument("rows",type=int,nargs="?",default=-1,help="Cantidad de registros a usar. DEFAULT todos")
	args = args.parse_args()
	quitaPrivadas(args)        