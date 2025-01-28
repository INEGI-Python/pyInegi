import argparse as ag
import numpy as np
import folium as fol
import geopandas as geo
import webbrowser as wb

def WebMAP(**param): 
	capas = [None]
	for i in range(len(param['datos'])):
		style=dict()
		tmp = geo.read_file(param["datos"][i])
		CRS = tmp.crs.to_string()
		# Configrar los estilos según el tipo de geometría
		if param["tipos"][i].upper() == "POINT":
			style = dict(
				radius=2,
				color=param["color"][i],
				weight=1,
				opacity=1,
				fillOpacity=0.7
			)
		else:  # Para LINESTRING, POLYGON, etc.
			style = dict(
				color=param["color"][i],
				weight=3,
				opacity=1
			)	
		capas.append(tmp.explore(
			m=capas[-1],
			name=param["names"][i],
			tooltip=True,
			style_kwds=style
		))
	fol.TileLayer("OpenStreetMap",show=True).add_to(capas[-1])
	fol.LayerControl().add_to(capas[-1])
	capas[-1].show_in_browser()
    

if __name__ == "__main__":
	parser = ag.ArgumentParser(description="Genera un Mapa Web de las capas de datos que el usuario cargue. Soporta ShapeFile, FeatureClass, GeoJson ")
	parser.add_argument('datos',type=str, help="Ruta absoluta o relativa  de las fuentes de Datos sepradas por comas")
	parser.add_argument('tipos',type=str,  help="Tipo de geometria. POINT, LINESTRING,POLYGON,MULTILINESTRING,MULTIPOLYGON, separadas por  comas respectivamente con las  fuentes de datos")
	parser.add_argument("nombres",type=str, nargs='?', default="Layer", help="Nombre con el  que apareceran en el mapa")
	parser.add_argument("color",type=str, nargs='?', default="black", help="Color de los elementos a mostrar")
	args = parser.parse_args()
	datos = args.datos.split(",")
	tipos  = args.tipos.split(",")
	names = args.nombres.split(",")       
	color = args.color.split(",")           
	if len(datos)!=len(tipos):
		print("[ERROR] La cantidad de fuentes datos no coincide con la cantidad de tipos")
		exit()
	if len(names)>1 and  len(names)!=len(datos):
		print("[ERROR] La cantidad de propiedades no coincide con la cantidad de datos")
		exit()
	if len(names)==1 and  len(names)!=len(datos):
	
		WebMAP(datos=datos,tipos=tipos,names=names*len(datos),color=color)
	else:
		WebMAP(datos=datos,tipos=tipos,names=names,color=color)
	




	##  pyInegi.generalizacion.webMap(datos=["DatosSalida/borde.shp","DatosSalida/lineaCentral.shp"],tipos=["LINESTRING","LINESTRING"],names=["¨Poñigono manzanas","Lineas Centrales"],color=["red","blue"])