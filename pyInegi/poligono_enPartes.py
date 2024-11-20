from arcpy.management import FeatureToPolygon as f2p, MakeFeatureLayer as mFl,MultipartToSinglepart as mPsP, DeleteFeatures as dF, SelectLayerByAttribute as sByA, SelectLayerByLocation as sBy, Delete as d
from arcpy.da import UpdateCursor as uC, SearchCursor as sC
from arcpy import env,  CreateCartographicPartitions_cartography as cCp
from arcpy.analysis import Clip
import argparse
from time import time as t
import os


def avance(s,_ini):
	fin = t()
	print(f"[{float(fin-_ini)} seg]  {s}")
	return fin


def inicio_pP(a):
	print(a)
	ini = avance("Inicio",t())
	if a.GDB== "None":
		polTmp = f"{a.SRC[:-4]}_toPolygon.shp"
	else:
		env.workspace=a.GDB
		env.overwriteOutput = True
		polTmp = f"{a.SRC}_toPolygon"
	print(a.SRC,polTmp)
	f2p(a.SRC,polTmp)
	mFl(a.SRC,"layerIn")
	
	#cont_vtx = len([json.loads(row[1]) for row in sC(a.SRC,['OID@','SHAPE@JSON'])][0]["paths"][0])
	ini = avance("Cartografia Particiones",ini)
	d(a.DEST)
	cCp("layerIn","D:/misDocs/2025/Python/consumir-pyInegi/datos/tempo.shp",a.CANT,a.METH_PART)
	#mFl(a.DEST,"tempo")
	ini= avance("Eliminando poligonos exedentes",ini)
	mFl("D:/misDocs/2025/Python/consumir-pyInegi/datos/tempo.shp","layerTmp")
	sBy("layerTmp","INTERSECT","layerIn",1,"NEW_SELECTION","INVERT")
	dF("layerTmp")
	ini = avance("Recortar la parte que sale del pais",ini)
	Clip("layerTmp",polTmp,"D:/misDocs/2025/Python/consumir-pyInegi/datos/tempoClip.shp")
	mFl("D:/misDocs/2025/Python/consumir-pyInegi/datos/tempoClip.shp","tempoClip")
	ini = avance("Haciendo SinglePartes",ini)
	mPsP("tempoClip",a.DEST)
	ini = avance("Quitando poligonos muy pequeños",ini)
	mFl(a.DEST,"destLayer")
	sByA("destLayer","NEW_SELECTION","Shape_Length < 500")
	dF("destLayer")
	ini = avance("Fin",ini)
 
 
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Herramientas para dividir un poligono en muchos.')
	parser.add_argument('GDB', type=str, help='GeodataBase origen')
	parser.add_argument('SRC', type=str, help='Feature  o Shape a trabajar')
	parser.add_argument('DEST', type=str, nargs='?', default=None, help='Feature de Salida, en caso de ser necesario.')
	parser.add_argument('CANT', type=int, nargs='?', default=909,  help='Numero de Partes o de Vertices a segun el metodo de particion utilizado. [Funcion geomMinima]')
	parser.add_argument('METH_PART', type=str, nargs='?', default="FEATURES",  help='Numero de Partes o de Vertices a segun el metodo de particion utilizado. Default FEATURES [Funcion geomMinima]')
	args = parser.parse_args()
	env.overwriteOutput = True
	inicio_pP(args)