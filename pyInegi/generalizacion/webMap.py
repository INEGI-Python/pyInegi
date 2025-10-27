import argparse as ag
import numpy as np
import folium as fol
import geopandas as geo
import webbrowser as wb

def WebMAP(**param): 
	capas = [None]
	for i in range(len(param['datos'])):
		style=dict()
		tmp = geo.read_file(param["datos"][i],rows=param["rows"] if param.get("rows") else None)
		CRS = tmp.crs.to_string()
		# Configrar los estilos según el tipo de geometría
		if param["tipos"][i].upper() == "POINT":
			style = dict(radius=1,fillOpacity=0.5)
			for e in param["estilo"][i].keys():
				style[e]=param["estilo"][i][e]
		else:  # Para LINESTRING, POLYGON, etc.
			style = dict(stroke=True)
			for e in param["estilo"][i].keys():
				style[e]=param["estilo"][i][e]

		capas.append(tmp.explore(
			m=capas[-1],
			name=param["names"][i],
			tooltip=False,
			popup=True,
			style_kwds=style
		))
	fol.TileLayer("OpenStreetMap",show=True).add_to(capas[-1])
	fol.LayerControl().add_to(capas[-1])
	capas[-1].show_in_browser() if param['web']==1 else capas[-1]
	return True
    

if __name__ == "__main__":
	parser = ag.ArgumentParser(description="Genera un Mapa Web de las capas de datos que el usuario cargue. Soporta ShapeFile, FeatureClass, GeoJson ")
	parser.add_argument('datos',type=str, help="Ruta absoluta o relativa  de las fuentes de Datos sepradas por comas")
	parser.add_argument('tipos',type=str,  help="Tipo de geometria. POINT, LINESTRING,POLYGON,MULTILINESTRING,MULTIPOLYGON, separadas por  comas respectivamente con las  fuentes de datos")
	parser.add_argument("nombres",type=str, nargs='?', default="Layer", help="Nombres de las capas separadas por comas")
	parser.add_argument("estilo",type=str, nargs='?', default="red-black", help="Color de relleno-borde separados por comas. DEFAULT: red-black")
	parser.add_argument("web",type=int, nargs='?', default=1, help="Si es cero el grafico se mostrara en una ventana del sistema operativo")
	args = parser.parse_args()
	datos = args.datos.split(",")
	tipos  = args.tipos.split(",")
	names = args.nombres.split(",")       
	colores = args.estilos.split(",")           
	if len(datos)!=len(tipos):
		print("[ERROR] La cantidad de fuentes datos no coincide con la cantidad de tipos")
		exit()
	if len(names)>1 and  len(names)!=len(datos):
		print("[ERROR] La cantidad de propiedades no coincide con la cantidad de datos")
		exit()
	estilo = [dict(fillColor=c.split("-")[0],color=c.split("-")[1]) for c in colores]
	WebMAP(datos=datos,tipos=tipos,names=names,estilo=estilo,web=args.web)
