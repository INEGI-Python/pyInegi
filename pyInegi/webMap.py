import argparse as ag
import folium as fol

if __name__ == "__main__":
	parser = ag.ArgumentParser(description="Genera un Mapa Web de las capas de datos que el usuario cargue. Soporta ShapeFile, FeatureClass, GeoJson ")
	parser.add_argument('datos',type=str, help="Ruta absoluta o relativa  de la fuente de Datos")
	parser.add_argument('tipo',type=str,  nargs='?', choices=["POINT","LINESTRING","POLYGON","MULTILINESTRING","MULTIPOLYGON"], help="Tipo de geometria. POINT, LINESTRING,POLYGON,MULTILINESTRING,MULTIPOLYGON")
	parser.add_argument("capas",type=str, help="Ruta de los datos separados por comas")
	args = parser.parse_args()
	print(args)