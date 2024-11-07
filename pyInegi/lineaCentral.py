import os
import numpy as np
import geopandas as pan
import  matplotlib.pyplot as plot
import folium
from shapely.geometry import LineString,Polygon,Point,GeometryCollection
from scipy.spatial import Voronoi
import argparse 

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
	else:
		_dat.to_file(name)

def inicio_lc(**_d):
	_data = pan.read_file(_d["gdb"],layer=_d["feat"]) if _d["gdb"][-3:]=="gdb" else   pan.read_file(_d["gdb"])
	CRS = _data.crs.to_string()
	_data.plot()
	pol,_result,id=1,[],1
	for d in _data.geometry:
		cen = Centro(d,_d["dist"])
		tmp=cen.createCenterline()
		for geo in tmp:
			_result.append({"id":id,"pol":pol,"geometry":geo,"crs":CRS})
			id+=1
		pol+=1
	_todo=pan.GeoDataFrame(data=_result,crs=CRS)
	if not os.path.exists("DatosSalida"): 
		os.mkdir("DatosSalida")
	crearArchivo(_todo,"DatosSalida/centerLineSalida.shp")
	if _d["ver"]==1:
		m = _todo.explore(tooltip=True,name="Linea Central")
		_data.explore(m=m,name="Poligonos",color="red")
		folium.TileLayer("OpenStreetMap",show=True).add_to(m)
		folium.LayerControl().add_to(m)
		m.show_in_browser()


if __name__=='__main__':
	parser = argparse.ArgumentParser(description="Devuelve la línea central de un polígono")
	parser.add_argument('GDB',type=str, help="Ruta absoluta o relativa  de  una Geodatabase o un Shapefile")
	parser.add_argument('FEAT',type=str,  nargs='?', default="fiona.listlayers(args.GDB)", help="Nombre del Featureclass o coloques un guion bajo (_) si no aplica. Si lo omite, el sistema le mostrara un listado de los featuresClass que contiene su geodatabase")
	parser.add_argument("CAMP",type=str, nargs='?', default=["*"], help="Arreglo de campos a obtener de sus datos")
	parser.add_argument("DIST",type=int, nargs='?', default=10, help="Distancia entre vertices para la densificación")
	parser.add_argument("VER",type=int, nargs='?', default=1, help="Genera y muestra un Mapa con el resultado. Default: 1")

	args = parser.parse_args()
	if args.FEAT=="fiona.listlayers(args.GDB)":
		import fiona
		print(eval(args.FEAT))
	else:
		inicio_lc(gdb=args.GDB,feat=args.FEAT,camp=args.CAMP,dist=args.DIST,ver=args.VER)