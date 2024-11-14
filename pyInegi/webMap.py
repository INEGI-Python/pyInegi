import argparse as ag
import folium as fol

if __name__ == "__main__":
	parser = ag.ArgumentParser(description="Genera un Mapa Web de las capas de datos que el usuario cargue. Soporta ShapeFile, FeatureClass, GeoJson ")
	parser.add_argument('datos',type=str, help="Ruta absoluta o relativa  de las fuentes de Datos sepradas por comas")
	parser.add_argument('tipos',type=str,  choices=["POINT","LINESTRING","POLYGON","MULTILINESTRING","MULTIPOLYGON"], help="Tipo de geometria. POINT, LINESTRING,POLYGON,MULTILINESTRING,MULTIPOLYGON, separadas por  comas respectivamente con las  fuentes de datos")
	parser.add_argument("props",type=str, nargs='?', default="{'name':'Layer1','color':'red','tooltips':True,'popups':True}", help="Objetos separados por comas con  las propiedades principales de cada Layer. Defualt: {'name':'Layer1','color':'red','tooltips':True,'popups':True} ")
	args = parser.parse_args()
	print(args)