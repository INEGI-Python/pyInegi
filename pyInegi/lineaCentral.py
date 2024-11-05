import os
import numpy as np
import geopandas as pan
import  matplotlib.pyplot as plot
from shapely.geometry import LineString,Polygon,Point,GeometryCollection

from scipy.spatial import Voronoi
import argparse 
from polyskel import skeletonize
from funciones import unir
from multiprocessing import Pool

class Centro(object):
		def __init__(self, inputGEOM, dist):
			self.inputGEOM = inputGEOM
			self.dist = abs(dist)

		def createCenterline(self):
			minx = int(min(self.inputGEOM.envelope.exterior.xy[0]))
			miny = int(min(self.inputGEOM.envelope.exterior.xy[1]))
			border = np.array(self.densifyBorder(self.inputGEOM, minx, miny))

			vor = Voronoi(border)
			vertex = vor.vertices

			lst_lines = []
			for j, ridge in enumerate(vor.ridge_vertices):
				if -1 not in ridge:
					line = LineString([
						(vertex[ridge[0]][0] + minx, vertex[ridge[0]][1] + miny),
						(vertex[ridge[1]][0] + minx, vertex[ridge[1]][1] + miny)])
					if line.within(self.inputGEOM) and len(line.coords[0]) > 1:
						lst_lines.append(line)
			return lst_lines

		def densifyBorder(self, polygon, minx, miny):
			if len(polygon.interiors) == 0:
				exterIN = LineString(polygon.exterior)
				points = self.fixedInterpolation(exterIN, minx, miny)
			else:
				exterIN = LineString(polygon.exterior)
				points = self.fixedInterpolation(exterIN, minx, miny)
				for j in range(len(polygon.interiors)):
					interIN = LineString(polygon.interiors[j])
					points += self.fixedInterpolation(interIN, minx, miny)
			return points
		def fixedInterpolation(self, line, minx, miny):
			count = self.dist
			newline = []
			startpoint = [line.xy[0][0] - minx, line.xy[1][0] - miny]
			endpoint = [line.xy[0][-1] - minx, line.xy[1][-1] - miny]
			newline.append(startpoint)
			while count < line.length:
				point = line.interpolate(count)
				newline.append([point.x - minx, point.y - miny])
				count += self.dist
			newline.append(endpoint)
			return newline

def crearArchivo(_dat,name):
	noms = name.split(".")
	if os.path.exists(name):
		newName = (noms[0][:-1] + str(int(noms[0][-1]) + 1) if noms[0][-1].isdigit() else f"{noms[0]}_1")
		_dat.to_file(f"{newName}.{noms[1]}")
  
def procesar(_geom): 
	print(_geom)
	print(os.pid(),_geom)
	_lin,skeleton=[],{"lin":[],"cen":[]}
	skeleton = skeletonize(_geom,1)
	print(f"PROCESO  ---> {os.pid()}")
	_lin=[x for x in [unir(l,skeleton["cen"]) for l in skeleton["lin"]] if x] 
	if len(_lin)>0:
		return _lin


def inicio_lc(**_d):
	_data = pan.read_file(_d["gdb"],layer=_d["feat"]) if _d["gdb"][-3:]=="gdb" else   pan.read_file(_d["gdb"])  
	crearArchivo(_data,"poligonos.shp")
	CRS = _data.crs.to_string()
	_data.plot()
	# _todo=[]
	# for d in _data.geometry:
	# 	cen = Centro(d,_d["dist"])
	# 	_result=cen.createCenterline()
	# 	_todo.append(_result)
	features = _data.geometry.__geo_interface__['features']
	feat_list = [list(f['geometry']['coordinates'][0]) for f in features]
	with Pool(4) as pool:
		res = pool.map(procesar,feat_list)
		pool.close()
		print(res)
	


if __name__=='__main__':
	parser = argparse.ArgumentParser(description="Devuelve la línea central de un polígono")
	parser.add_argument('GDB',type=str, help="Ruta absoluta o relativa  de  una Geodatabase o un Shapefile")
	parser.add_argument('FEAT',type=str,  nargs='?', default="fiona.listlayers(args.GDB)", help="Nombre del Featureclass o coloques un guion bajo (_) si no aplica. Si lo omite, el sistema le mostrara un listado de los featuresClass que contiene su geodatabase")
	parser.add_argument("CAMP",type=str, nargs='?', default=["*"], help="Arreglo de campos a obtener de sus datos")
	parser.add_argument("DIST",type=int, nargs='?', default=100, help="Distancia entre vertices para la densificación")
	parser.add_argument("VER",type=int, nargs='?', default=1, help="Genera y muestra un Mapa con el resultado. Default: 1")

	args = parser.parse_args()
	if args.FEAT=="fiona.listlayers(args.GDB)":
		import fiona
		print(eval(args.FEAT))
	else:
		inicio_lc(gdb=args.GDB,feat=args.FEAT,camp=args.CAMP,dist=args.DIST,ver=args.VER)