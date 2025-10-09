from itertools import count
import os
import shutil
import geopandas as geo
import   pandas as pan
import fiona
import argparse
import rasterio

def gdb2gpkg(gdb_path, gpks_path,bati):
	layers = fiona.listlayers(gdb_path)
	for layer in layers:
		gdf = geo.read_file(gdb_path, layer=layer)
		gdf.to_file(gpks_path, layer=layer, driver="GPKG")
	print(bati)
	if os.path.exists(bati):
		with rasterio.open(bati) as src:
			print(dir(src))
			rasterio.open(gpks_path,'w',driver="GPKG",width=src.width,height=src.height,count=src.count,dtype=src.dtype, crs=src.crs,transform=src.transform,layer="batimetriasombreado").write(src.read(),indexes=1)

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
			try:
				orient = str(excel[excel['NOMGEO']==ent]["Orientacion"].values[:])[2:-2]
				print(f"{ent}  -  {orient}")
				shutil.copy2(f"{tmpl}/{orient}.qgz",f"{dst_dir}/{ent}.qgz")
				if os.path.exists(f"{root}/batimetriasombreado.tif"):
					print(os.path.exists(f"{root}/batimetriasombreado.tif"))		
					shutil.copy2(f"{root}/batimetriasombreado.tif",f"{dst_dir}/batimetriasombreado.tif")
				gdb2gpkg(gdb,gpk,f"{dst_dir}/batimetriasombreado.tif")
			except Exception as e:
				print(e)
		dirs[:] = [d for d in dirs if not d.lower().endswith('.gdb')]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convierte una geodatabase (GDB) a un GeoPackage (GPKG).")
	parser.add_argument("--version", action="version", version="gdb2gpkg 1.0")
	parser.add_argument("--verbose", action="store_true", help="Muestra información detallada durante la ejecución.")
	parser.add_argument("datos",type=str, help="Carpeta de los datos de  origen")
	parser.add_argument("plantilla",type=str,help="Carpeta donde se encuentran las plantillas y el excel")
	args = parser.parse_args()

	copy_without_gdb(args.datos, f"{args.datos}_GPKG",args.plantilla)




