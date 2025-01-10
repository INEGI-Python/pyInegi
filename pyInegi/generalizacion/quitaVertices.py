# -*- coding: utf-8 -*-
#from arcpy.da import UpdateCursor as uC, SearchCursor as sC
#from arcpy import env,Array as arr, Geometry as geo,  Point as p


from ctypes import alignment
import geopandas as geo
import argparse


#def inicio_arcpy(_gdb,feat1,feat2):
#	def tipo(_t):
#		return {"MultiLineString":"polyline","LineString":"polyline","MultiPolygon":"polygon","Polygon":"polygon"}[_t]
#	env.workspace=_gdb
#	quitar = [c[1]  for c in sC(feat2,['OID@','SHAPE@XY'])]
#	with uC(feat1,['OID@','SHAPE@']) as Cursor:
#		rows = Cursor.next()
#		_t=rows[1].__geo_interface__["type"]
#		geom = rows[1].__geo_interface__["coordinates"][0]
#		[geom.remove(vtx) for vtx in quitar if vtx in geom]
#		rows[1] = geo(tipo(_t),arr([p(*c) for c in geom]))
#		Cursor.updateRow(rows)


def inicio_gpd(**param):
	print(param)
	gdf1 = geo.read_file(param['shp1']) if param.get('gdb1') is None else  geo.read_file(param['gdb1'],layer=param['feat1'])
	gdf2 = geo.read_file(param['shp2']) if param.get('gdb2') is None else  geo.read_file(param['gdb2'],layer=param['feat2'])
	inter= gdf2.intersection(gdf1,align=True)
	print(inter)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Quitar vertices especificos')
	parser.add_argument('shp1', type=str, nargs='?', default=None, help='Archivo ShapeFile donde  se encuentran los datos a trabajar')
	parser.add_argument('shp2', type=str, nargs='?', default=None, help='Archivo ShapeFile de Puntos donde  se encuentran los datos a eliminar')
	
	parser.add_argument('gdb1', type=str, nargs='?', default=None, help='GeodataBase donde  se encuentran los datos a trabajar')
	parser.add_argument('feat1', type=str, nargs='?', default=None, help='FeatureClass de los datos a trabajar')

	parser.add_argument('gdb2', type=str, nargs='?', default=None, help='GeodataBase donde  se encuentran los datos a eliminar')
	parser.add_argument('feat2', type=str, nargs='?', default=None, help='FeatureClass de Puntos a eliminar')

	a = parser.parse_args()
	
	inicio_gpd(gdb1=a.gdb1,feat1=a.feat1,shp1=a.shp1,gdb2=a.gdb2,feat2=a.feat2,shp2=a.shp2)
	#inicio_arcpy(args.GDB,args.SRC,args.QUITAR)