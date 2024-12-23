import os
from time import time as t
import folium
import geopandas
import numpy as np
from multiprocessing import Pool
from shapely.geometry import LineString,MultiLineString,shape,Point
from scipy.spatial import Voronoi
#import topojson
import argparse
from pyInegi.shapely_tools import intersection_points


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

def multi(pol):
    print(f"[PID: {os.getpid()}] Poligono: {pol[0]}...",end="")
    ini=t()
    a =  Centro(pol,10)
    tmp = a.createCenterline()
    geoms = shapely.multilinestrings([shapely.LineString(t.__geo_interface__["coordinates"]) for t in tmp])
    del a
    print(f"..... {t()-ini}")
    return {"pol":pol, "geometry":geoms.simplify(0.00001)}


def inicio(a):
	ini=t()
	orig =  geopandas.read_file(a.file,rows=a.rows)
	orig.set_index("OBJECTID",inplace=True)
	CRS = orig.crs.to_string()
	segm = orig.segmentize(a.dist)
	voroPoly = segm.voronoi_polygons()
	borde = segm.boundary
	voroClip=voroPoly.boundary.clip(orig)
	union = voroClip.union_all()
	linSep=list(union.geoms)
	df = geopandas.GeoDataFrame(geometry=linSep,crs=CRS)
	inter,ids=intersection_points(linSep,list(borde.iloc[0].geoms),0.1)
	df=df.drop(index=ids)
	Central = df.union_all("unary")
	df_union = geopandas.GeoDataFrame(geometry=[Central],crs=CRS)
	borde.to_file(renombrar("DatosSalida/borde.shp"))
	df_union.to_file(renombrar("DatosSalida/noRepeat.shp"))



	puntosInter = geopandas.GeoDataFrame(geometry=inter,crs=CRS)
	puntosInter.to_file(renombrar("DatosSalida/Intersecciones.shp"))
	
	# casiCentral.to_file("DatosSalida/voronoi_2.shp")
	# extDF.to_file("DatosSalida/PoligonoExterno.shp")
	
	# #geopandas.GeoDataFrame({"geometry":shapely.linestrings(x_lin_ext),"crs":CRS}).to_file("DatosSalida/LineaExt.shp")
	# inter=capa1.intersects(x_lin_ext)
	# #print(inter)
	# eliminar = [i for i,n in enumerate(inter) if n]
	# print(eliminar)
	# capa1.drop(index=eliminar)
	# capa1.to_file("DatosSalida/voronoi_CENTRAL.shp")
    # #print([z for z in capa1.iterrows() if z in inter])
	m = puntosInter.explore(name="Interseccion",color="blue")
	m0 = borde.explore(m=m,name="Poligonos Exteriores",color="red")
	m1 = df_union.explore(m=m0,name="Voronoi Central",color="black", tooltip=True)
	folium.TileLayer("OpenStreetMap",show=True).add_to(m1)
	folium.LayerControl().add_to(m1)
	m1.show_in_browser()
    
    
    
    # 
    # with Pool() as pool:
    #     dat = pool.map(multi,x.iterrows())
        
    #     print(f"TIEMPO TOTAL: {float(t()-ini)}")
    #     _d = geopandas.GeoDataFrame(data=dat,crs=CRS)
    #     topo = topojson.Topology(_d)
    #     topo_smooth = topo.toposimplify(0.1)
    #     _df = topo_smooth.to_gdf()
    #     _df.to_file(renombrar("DatosSalida/centerSalida.shp"))

class argumentos:
	def __init__(self,f,r,d):
		self.file=f
		self.rows=r
		self.dist=d
args = argumentos("prueba3.shp",2,5)
inicio(args)

if False: # __name__ == "__main__":
    args = argparse.ArgumentParser(description="Regresa  las lineas centrales de cualquier poligono")
    args.add_argument("file",type=str,nargs="?",default="prueba3.shp",help="Ruta de la capa de poligonos")
    args.add_argument("rows",type=int,nargs="?",default=5,help="Cantidad de registros a usar. Default todos")
    args.add_argument("dist",type=int,nargs="?",default=10,help="Longitud maxima de las lineas al segmentar")
    
    args = args.parse_args()
    inicio(args)        

        
# import pyInegi

# f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
# f.run(gdb='MOPIGMA.gdb', feat='prueba2', camp=["*"],dist=15,ver=1)
