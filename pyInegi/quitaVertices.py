# -*- coding: utf-8 -*-
from arcpy.da import UpdateCursor as uC, SearchCursor as sC
from arcpy import env,Array as arr, Geometry as geo,  Point as p
import argparse

def inicio_qV(_gdb,feat1,feat2):
	def tipo(_t):
		return {"MultiLineString":"polyline","LineString":"polyline","MultiPolygon":"polygon","Polygon":"polygon"}[_t]
	env.workspace=_gdb
	quitar = [c[1]  for c in sC(feat2,['OID@','SHAPE@XY'])]
	with uC(feat1,['OID@','SHAPE@']) as Cursor:
		rows = Cursor.next()
		_t=rows[1].__geo_interface__["type"]
		geom = rows[1].__geo_interface__["coordinates"][0]
		[geom.remove(vtx) for vtx in quitar if vtx in geom]
		rows[1] = geo(tipo(_t),arr([p(*c) for c in geom]))
		Cursor.updateRow(rows)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Quitar vertices especificos')
	parser.add_argument('GDB', type=str, help='GeodataBase origen')
	parser.add_argument('SRC', type=str, help='Feature a trabajar. (NO puntos)')
	parser.add_argument('QUITAR', type=str, help='Feature de puntos a quitar')
	args = parser.parse_args()

	inicio_qV(args.GDB,args.SRC,args.QUITAR)