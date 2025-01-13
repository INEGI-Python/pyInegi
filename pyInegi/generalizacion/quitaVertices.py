# -*- coding: utf-8 -*-
#from arcpy.da import UpdateCursor as uC, SearchCursor as sC
#from arcpy import env,Array as arr, Geometry as geo,  Point as p
from os import getcwd
import numpy as np
import geopandas as geo
import argparse
from shapely.geometry import Polygon
from ..basico.funciones import renombrar

def QuitaVertices(**param):
	gdf1 = geo.read_file(param['shp1']) if param.get('gdb1') is None else  geo.read_file(param['gdb1'],layer=param['feat1'])
	gdf2 = geo.read_file(param['shp2']) if param.get('gdb2') is None else  geo.read_file(param['gdb2'],layer=param['feat2'])
	CRS = gdf1.crs.to_string()
	# Obtener los vértices que se intersectan
	vertices_gdf1 = gdf1.exterior.apply(lambda x: list(x.coords))
	vertices_gdf2 = gdf2.geometry.apply(lambda x: (x.x, x.y)).tolist()
	vtx_new = []
	for poly_vertices in vertices_gdf1:
		for vertice in poly_vertices:
			if vertice not in vertices_gdf2:
				vtx_new.append(np.asarray(vertice))
	new_pol = geo.GeoDataFrame(geometry=[Polygon(vtx_new)],crs=CRS)
	new_nom = renombrar("DatosSalida/resQuitaVtx.shp")
	new_pol.to_file(new_nom)
	print(f"El o los objetos resultantes se encuentran en --> {getcwd()}/{new_nom}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="quitaVertices",description='Quitar vertices especificos')
	parser.add_argument('shp1', type=str, nargs='?', default=None, help='Archivo ShapeFile donde  se encuentran los datos a trabajar')
	parser.add_argument('shp2', type=str, nargs='?', default=None, help='Archivo ShapeFile de Puntos donde  se encuentran los datos a eliminar')
	
	parser.add_argument('gdb1', type=str, nargs='?', default=None, help='GeodataBase donde  se encuentran los datos a trabajar')
	parser.add_argument('feat1', type=str, nargs='?', default=None, help='FeatureClass de los datos a trabajar')

	parser.add_argument('gdb2', type=str, nargs='?', default=None, help='GeodataBase donde  se encuentran los datos a eliminar')
	parser.add_argument('feat2', type=str, nargs='?', default=None, help='FeatureClass de Puntos a eliminar')

	a = parser.parse_args()
	
	QuitaVertices(gdb1=a.gdb1,feat1=a.feat1,shp1=a.shp1,gdb2=a.gdb2,feat2=a.feat2,shp2=a.shp2)