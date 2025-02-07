from re import A
import geopandas as geo
import rtree
from scipy.fft import set_global_backend
from shapely import Point

#def agrupar_lineas(lineas, puntos,CRS):
    # Crear un índice espacial para las líneas
	# index = rtree.index.Index()
	# for i, line in enumerate(lineas.geometry):
	# 	index.insert(i, line.bounds)

    # Crear un GeoDataFrame vacío para almacenar las líneas agrupadas
	#lineas_agrupadas = geo.GeoDataFrame(columns=["OBJECTID","geometry"], crs=CRS)

    # Iterar sobre los puntos y agrupar las líneas que se tocan
	# def encontrar_lineas_conectadas(punto, lineas, index,ids):
	# 	temp = list(index.intersection(punto.bounds))
	# 	print(ids)
	# 	posibles_lineas = [i for i in temp if i not in ids]
	# 	print(posibles_lineas)
	# 	lineas_a_agrupar = lineas.iloc[posibles_lineas]
	# 	if lineas_a_agrupar.empty:
	# 		return posibles_lineas
	# 	tmp = []
	# 	for la in lineas_a_agrupar.geometry:
	# 		print(la.coords[0])
	# 		print(punto)
	# 		punto = Point(la.coords[-1] if punto == la.coords[-1] else la.coords[0])
	# 		print(punto)
	# 		input()
	# 		ids.extend(encontrar_lineas_conectadas(punto, lineas, index,
    #                                       ))
	# 	return ids
    # # Iterar sobre los puntos y agrupar las líneas que se tocan
	# for punto in puntos.geometry:
	# 	ids=[]
	# 	ids = encontrar_lineas_conectadas(punto, lineas, index,ids)
	# 	print(ids)
	# 	lineas_agrupadas = lineas_agrupadas._append({"geometry": lineas.iloc[ids].geometry}, ignore_index=True)
	# return lineas_agrupadas

class arbol:
	def __init__(self,id,punto):
		self.id=id
		self.punto = punto
		self.geom = geom
		self.ramas = []
	def agregar_rama(self,r):
		self.ramas.append(r)

class rama:
    def __init__(self,id,geom):
        self.id=id
        self.geom = geom
		self.hojas = []


class hoja:
	def __init__(self,id,rama,geom):
		self.id=id
		self.geom=geom

def invierteLineasHidro(**a):
	lineas = geo.read_file(a["lineas"],columns=["OBJECTID","geometry"])
	puntos = geo.read_file(a["puntos"],columns=["geometry"])
	CRS = lineas.crs.to_string()
    # Agrupar las líneas que se tocan
	lineas_agrupadas = agrupar_lineas(lineas, puntos,CRS)

    # Guardar el resultado en un archivo shapefile
	lineas_agrupadas.to_file("DatosSalida/lineas_agrupadas.shp")


if __name__ == "__main__":
	invierteLineasHidro(lineas="DatosEntrada/lineasHidro.shp", puntos="DatosEntrada/puntos_dren.shp")