from itertools import count
import os
import shutil
import geopandas as geo
import   pandas as pan
import argparse
import fiona





def crearRaster(tif):
	os.system(f"C:/Program Files/QGIS 3.40.10/bin/gdal_translate.exe -of GPKG -b 3 {tif} batimetriasombreado.gpkg")



def crearGPKG(esquema,crs,nom,features):
	with fiona.open(nom,'w',driver='GPKG',crs=crs,schema=esquema) as datos:
		for f in features:
			datos.write(f)
		return datos


def gdb2gpkg(gdb_path, gpks_path,_root,bati):
	os.system(f"\"C:/Program Files/QGIS 3.40.10/bin/gdal_translate.exe\" -of GPKG -b 3 {tif} {gpks_path.replace("mapa_base.gpkg","batimetriasombreado.gpkg")}")
	layers = fiona.listlayers(gdb_path)
	for layer in layers:
		gdf = geo.read_file(gdb_path, layer=layer)
		gdf.to_file(gpks_path, layer=layer, driver="GPKG")
	print("BATI   ",f"{_root}/{bati}")
	if bati is not None:
		with  ras.open(f"{_root}/{bati}","r") as tif:
			geopack = f"{os.getcwd()}/img.gpkg"
			print(geopack)
			lay = ras.open(geopack,'w', driver="GPKG")

def gdb2gpkg(gdb_path, gpks_path,tif):
	tmp = gpks_path.replace("mapa_base.gpkg","batimetriasombreado.gpkg")
	os.system(f"\"C:/Program Files/QGIS 3.40.10/bin/gdal_translate.exe\" -of GPKG -b 3 {tif} {tmp}")
	os.system(f"REN  {tmp}  {gpks_path}")
	layers = fiona.listlayers(gdb_path)
	for layer in layers:
		gdf = geo.read_file(gdb_path, layer=layer)
		gdf.to_file(gpks_path, layer=layer, driver="GPKG")

			
 			
			# print(tif.profile)
			# profile=tif.profile
			# profile.update(driver='GPKG', **{'Bike_size':'Tiled'} )
			# with ras.open("img.gpkg",'w', **profile) as dts:
			# 	dts.write(tif.read(),indexes=1)
			# 	dts.write_tile(tif.read(),indexex=1)
			# 	dts.set_bounds(raster_bounds(tif))
			# 	dts.set_crs(tif.crs)
			# 	dts.set_name("batimetriasombreado")
	


def copy_without_gdb(src, dst,tmpl):
	excel = pan.read_excel(f"{tmpl}/Caneva_Estados.xlsx",index_col=0)
	excel.sort_index(inplace=True)
	for root, dirs, files in os.walk(src):
		root=root.replace("\\","/")
		rel_path = os.path.relpath(root, src)
		dst_dir = os.path.join(dst, rel_path).replace("\\","/")
		os.makedirs(dst_dir, exist_ok=True)
		if root==src:
			x=dirs
		else:
			gdb = f"{root}/{str(dirs)[2:-2]}"
			gpk = f"{dst_dir}/{str(dirs)[2:-5]}gpkg"
			ent=root.split("/")[-1]
			orient = str(excel[excel['NOMGEO']==ent]["Orientacion"].values[:])[2:-2]
			print(f"{ent}  -  {orient}")
			shutil.copy2(f"{tmpl}/{orient}.qgz",f"{dst_dir}/{ent}.qgz")
			bati = [f for f in files if f.endswith(".tif")]
			bati = bati[0] if len(bati)>0 else None
			gdb2gpkg(gdb,gpk,bati)
		dirs[:] = [d for d in dirs if not d.lower().endswith('.gdb')]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convierte una geodatabase (GDB) a un GeoPackage (GPKG).")
	parser.add_argument("--version", action="version", version="gdb2gpkg 1.0")
	parser.add_argument("--verbose", action="store_true", help="Muestra información detallada durante la ejecución.")
	parser.add_argument("datos",type=str, help="Carpeta de los datos de  origen")
	parser.add_argument("plantilla",type=str,help="Carpeta donde se encuentran las plantillas y el excel")
	args = parser.parse_args()


	copy_without_gdb(args.datos, f"{args.datos}_GPKG",args.plantilla)


# esquema={'geometry':'Point','properties':{'name':'str','value':'int'}}
# feats=[{'geometry':{'type':'Point','coordinates':(10.0,20.0)},'properties': { 'name':'Elemento1','value':1000}},{'geometry':{'type':'Point','coordinates':(20.0,30.0)},'properties': { 'name':'Elemento2','value':2000}}]
# myData = crearGPKG(esquema,'EPSG:4326',"miGeopaquete.gpkg",feats)



