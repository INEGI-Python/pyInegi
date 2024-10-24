import geopandas as pan
import argparse 

def inicio(**_d):
	_data = pan.read_file(_d["gdb"],layer=_d["feat"]) if _d["gdb"][-3:]=="gdb" else   pan.read_file(_d["gdb"])
	print(_data)
	if _d["ver"]==1:
		_data.plot()

if __name__=='__main__':
	parser = argparse.ArgumentParser(description="Devuelve la línea central de un polígono")
	parser.add_argument('GDB',type=str, help="Ruta absoluta o relativa  de  una Geodatabase o un Shapefile")
	parser.add_argument('FEAT',type=str,  nargs='?', default="fiona.listlayers(args.GDB)", help="Nombre del Featureclass o coloques un guion bajo (_) si no aplica. Si lo omite, el sistema le mostrara un listado de los featuresClass que contiene su geodatabase")
	parser.add_argument("CAMP",type=str, nargs='?', default="[*]", help="Arreglo de campos a obtener de sus datos")
	parser.add_argument("VER",type=int, nargs='?', default=1, help="Genera y muestra un Mapa Web con el resultado. Default: 1")

	args = parser.parse_args()
	if args.FEAT=="fiona.listlayers(args.GDB)":
		import fiona
		print(eval(args.FEAT))
	else:
		inicio(gdb=args.GDB,feat=args.FEAT,camp=args.CAMP,ver=args.VER)