import os,sys
import geopandas as geo

def gdb2gpkg(gdb_path, gpks_path):
	if not os.path.exists(gdb_path):
		raise FileNotFoundError(f"La geodatabase {gdb_path} no existe.")
	
	if os.path.exists(gpks_path):
		raise FileExistsError(f"El archivo GeoPackage {gpks_path} ya existe.")
	
	os.getcwd()
	gdb_gdf = geo.read_file(gdb_path)
	gdb_gdf.to_file(gpks_path, driver="GPKG")

	gdb_driver = ogr.GetDriverByName("OpenFileGDB")
	gdb = gdb_driver.Open(gdb_path, 0)
	if gdb is None:
		raise RuntimeError(f"No se pudo abrir la geodatabase {gdb_path}.")
	
	gpks_driver = ogr.GetDriverByName("GPKG")
	gpks = gpks_driver.CreateDataSource(gpks_path)
	if gpks is None:
		raise RuntimeError(f"No se pudo crear el GeoPackage {gpks_path}.")
	
	for i in range(gdb.GetLayerCount()):
		layer = gdb.GetLayerByIndex(i)
		layer_name = layer.GetName()
		print(f"Procesando capa: {layer_name}")
		
		gpks_layer = gpks.CreateLayer(layer_name, geom_type=layer.GetGeomType(), srs=layer.GetSpatialRef())
		if gpks_layer is None:
			print(f"No se pudo crear la capa {layer_name} en el GeoPackage.")
			continue
		
		layer_defn = layer.GetLayerDefn()
		for j in range(layer_defn.GetFieldCount()):
			field_defn = layer_defn.GetFieldDefn(j)
			gpks_layer.CreateField(field_defn)
		
		gpks_layer_defn = gpks_layer.GetLayerDefn()
		
		for feature in layer:
			new_feature = ogr.Feature(gpks_layer_defn)
			new_feature.SetFrom(feature)
			gpks_layer.CreateFeature(new_feature)
			new_feature.Destroy()
		
		print(f"Capa {layer_name} procesada y guardada en el GeoPackage.")
	
	gdb.Destroy()
	gpks.Destroy()
	print(f"Conversión completada. Archivo guardado en {gpks_path}")

import argparse
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convierte una geodatabase (GDB) a un GeoPackage (GPKG).")
	parser.add_argument("gdb_path", type=str, help="Ruta al archivo de geodatabase (.gdb)")
	parser.add_argument("gpks_path", type=str, help="Ruta al archivo de salida GeoPackage (.gpkg)")
	
	args = parser.parse_args()
	
	try:
		gdb2gpks(args.gdb_path, args.gpks_path)
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)
