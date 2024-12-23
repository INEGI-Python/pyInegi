import os
from time import time as t
import geopandas,shapely
import numpy as np
from multiprocessing import Pool
from shapely.geometry import LineString,MultiLineString,shape
from scipy.spatial import Voronoi
import topojson
import argparse


def renombrar(name):
	noms = name.split(".")
	if not os.path.exists(name): 
		return name
	newName = (noms[0][:-1] + str(int(noms[0][-1]) + 1) if noms[0][-1].isdigit() else f"{noms[0]}_1")
	nomComp = f"{newName}.{noms[1]}"
	return renombrar(nomComp)

class Centro(object):
		def __init__(self, inputGEOM,dis):
			self.inputGEOM = inputGEOM
			self.dist=abs(dis)

		def createCenterline(self):
			minx = int(min(self.inputGEOM.envelope.exterior.xy[0]))
			miny = int(min(self.inputGEOM.envelope.exterior.xy[1]))
			border = self.densifyBorder(self.inputGEOM, minx, miny)
			#border=list(self.inputGEOM.__geo_interface__["coordinates"][0])
			#print(border)
			vor = Voronoi(np.array(border))
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

def multi(g,pol):
    print(f"[PID: {os.getpid()}] Poligono: {pol}...",end="")
    ini=t()
    a =  Centro(g,10)
    tmp = a.createCenterline()
    geoms = shapely.multilinestrings([shapely.LineString(t.__geo_interface__["coordinates"]) for t in tmp])
    del a
    print(f"..... {t()-ini}")
    return {"pol":pol, "geometry":geoms.simplify(0.00001)}


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Regresa  las lineas centrales de cualquier poligono")
    args.add_argument("file",type=str,help="Ruta de la capa de poligonos")
    args.add_argument("rows",type=int,nargs="?",default=None,help="Cantidad de registros a usar. Default todos")
    args = args.parse_args()
    inicio=t()
    x =  geopandas.read_file(args.file,rows=args.rows)
    x.convert_dtypes()
    id_pol=len(x.count_geometries()) if args.rows == None else list(range(args.rows))
    CRS = x.crs.to_string()
    x.plot()
    with Pool() as pool:
        dat = pool.starmap(multi,zip(x.geometry,id_pol))
        
        print(f"TIEMPO TOTAL: {float(t()-inicio)}")
        _d = geopandas.GeoDataFrame(data=dat,crs=CRS)
        topo = topojson.Topology(_d)
        topo_smooth = topo.toposimplify(0.1)
        _df = topo_smooth.to_gdf()
        _df.to_file(renombrar("DatosSalida/centerSalida.shp"))
    
    
        
        
        
# import pyInegi

# f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
# f.run(gdb='MOPIGMA.gdb', feat='prueba2', camp=["*"],dist=15,ver=1)

