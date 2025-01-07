# -*- coding: utf-8 -*-
import os
from time import time as t
from arcpy import env
from arcpy.da import SearchCursor as sC, InsertCursor as iC, UpdateCursor as uC
from arcpy.management import CopyFeatures as cpF, FeatureVerticesToPoints as fV, AddField as aF,CreateFeatureDataset as cFd,AddIndex as aI, RemoveIndex as rI
from arcpy import SpatialReference as sPt, Point as pt, Geometry as _aG, Array as aa
from multiprocessing import cpu_count,Pool
import argparse 
from ..funciones import  *
from ..polyskel import skeletonize


def memory_usage_psutil():
    import psutil
    import os
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / float(2 ** 20)
    return mem


def importarDatos(Datos):
	for i in range(1,Datos["totPol"],1):
		Datos['geomEnt'][i]={ 'cant':0,'coord':[]}
	with sC("tmp/nodos",["id_tmp","SHAPE@XY"]) as nodos:
		Datos['vtxTot'] = len(nodos._as_narray())
		nodos.reset()
		for n in nodos:
			Datos['geomEnt'][n[0]]['coord'].append(n[1])
			Datos['geomEnt'][n[0]]['cant'] +=1
	return Datos['geomEnt']

def distancia(p1,p2):
	dist = ((p2.X-p1.X)**2 + (p2.Y-p1.Y)**2)**0.5
	return dist
	
def par(lst):
	i = iter(lst)
	prev = next(i)
	for item in i:
		yield prev, item
		prev = item

	
def procesar(_geom,numPol,_x100): 
	print("%d -> \t %.1f \t %d" % (numPol,memory_usage_psutil(),os.getpid()),end="\t")
	_lin,skeleton=[],{"lin":[],"cen":[]}
	skeleton = skeletonize(_geom,numPol)
	print("%.2f %s" % (avance(_x100),"%"))
	_lin=[x for x in [unir(l,skeleton["cen"]) for l in skeleton["lin"]] if x] 
	if len(_lin)>0:
		return (numPol,_lin)


def inicio(_gdb,_fCls,distancia,cpu=cpu_count(),vtx=0,eps=0.001,apx=0.02):
	ini = t()
	Rutas = {'gdb':''}
	Datos = {'auxLineas':{},'contador':0,'totPol':0,'distancia':0,'geomEnt':{},'vtx':0,'vtxTot':0,'import':importarDatos,'porcAvance':0.00}
	if not _gdb[-3:]=="gdb":
		print("No selecciono una Geodatabase valida.")
		exit(1)
	env.workspace=_gdb
	env.overwriteOutput = True
	try:
		aF(_fCls,"id_tmp","LONG")
	except Exception as e:
		print(e)
	i = 1
	with uC(_fCls,["OBJECTID","id_tmp"]) as reIndex:
		for  row in  reIndex:
			row[1] = i
			reIndex.updateRow(row)
			i +=1
	Datos["totPol"]=i
	try:
		rI(_fCls,"_idx_id_tmp")
	except:
		pass
	aI(_fCls,"id_tmp","_idx_id_tmp",True,True)
	Rutas['_nom'] = _fCls.split("/")[1] if _fCls.replace("\\","/").find("/") > -1 else _fCls		
	Rutas['dSet'] = cFd(_gdb,"tmp",sPt(6372))
	fV(_gdb+"/"+_fCls,_gdb+"/tmp/nodos","ALL")
	aI(_gdb+"/tmp/nodos","id_tmp","_idx_nodos",True,True)

	Datos['distancia']=distancia
	Datos['vtx']=vtx
	Datos['cpu']= cpu
	Rutas['gdb']=_gdb
	Rutas['feat'] = _fCls
	Datos['geomEnt'] = Datos["import"](Datos)
	
	print("[%d  CPUs]  Ejecutando procedimiento con multiprocesos. " % Datos["cpu"])
	a=open("avance.aux","w")
	a.write("0.0")
	a.close()
	_keys = list(Datos['geomEnt'].keys())
	_keys.sort()
	ctrl = {}
	for k in _keys:
		ctrl[k]={}
	textFile("parametros.py","w","data={'dist':%.1f,'EPSILON':%f,'APROX':%f}" %(Datos['distancia'],eps,apx))
	pols = [Datos['geomEnt'][k]['coord'] for k in _keys]
	arr100 =  [(Datos['geomEnt'][k]['cant']*100)/Datos['vtxTot']  for k in _keys]
	auxLin = {}
	with Pool(Datos["cpu"]) as pool:
		res = pool.starmap(procesar,zip(pols,_keys,arr100))
		pool.close()
		for k,coord in [r for r in res if r is not None]:
			auxLin[k]=coord
	_key_ = list(auxLin.keys())
	Rutas['_nom_l'] = crearFeat(Rutas['dSet'],Rutas['_nom'],auxLin,_key_,'POLYLINE',"_Skeletor","numPol")
	cpF(Rutas['feat'] ,Rutas['gdb']+"/tmp/resultado")
	print("[%d áreas]  Ajustando la separacion de líneas... " % len(_key_) )
	resul = separar(Datos,Rutas,uC,sC,_aG,aa,pt)
	return t()-ini
	



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Separa el espacio entre la misma linea")
	parser.add_argument('GDB',type=str,  help="Ruta absluta o relativa de la geodabase")
	parser.add_argument('FEAT',type=str,  help="Ruta relativa a la geodabase donde se encuentra el FeatureClass o el FeatureDataSet/FeatureClass")
	parser.add_argument('DIST', type=int,  help="Distancia en metros del espacio minimo que debe existir entre la linea ")
	parser.add_argument('CPU',type=int, nargs='?', default=cpu_count(), help="Número de procesos u objetos que se ejecutaran en paralelo en un tiempo dado. Default y máximo %d para este equipo" %cpu_count())
	parser.add_argument('VTX',type=int, nargs='?', default=0, help="Numero de vertices a quitar antes y despues de una zona afectada. Default: 0 vertices")
	parser.add_argument('EPS',type=float, nargs='?', default=0.001, help="Valor de EPSILON. Defualt: 0.001")
	parser.add_argument('APX',type=float, nargs='?', default=0.02, help="Valor de aproximacion entre dos coordenadas. Defualt: 0.02")
	args = list(parser.parse_args().__dict__.values())

	tiempo=inicio(*args)
	print("Tiempo de ejecución: %.3f segundos" % tiempo)
	


#    %pro% Principal.py Separa.gdb Frontera/Mexico_enPartes 120  64 2 0.001 0.02
#     %pro% Principal.py Separa.gdb Frontera/Mexico_enPartes 120