from platform import processor
import os,shutil
import   pandas as pan
import argparse
import fiona

def gdb2gpkg(gdb_path, gpks_path,cond,tif):
	if os.path.exists(gpks_path):
		os.remove(gpks_path)

	layers = fiona.listlayers(gdb_path)
	for layer in layers:
		with fiona.open(gdb_path,'r',layer=layer) as capaOrigen:
			perfil = capaOrigen.profile
			perfil['driver']='GPKG'
			with fiona.open(gpks_path,'w',**perfil,layer=layer) as  capaDest:
				for elemento in capaOrigen:
					capaDest.write(elemento)
	print(f"Capas  copiadas con exito a {gpks_path.split('/')[-2]}" )
	if cond is not None:
		print("... agregando el raster de batimetria...")
		os.system(f'C:/Progra~1/QGIS34~1.10/bin/gdal_translate.exe -a_srs EPSG:4326  -of GPKG -co APPEND_SUBDATASET=YES -co RASTER_TABLE="batimetriasombreado"  {tif} {gpks_path}')
	
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
			shutil.copy2(f"{root}/INEGI_Logotipo_5.jpg",f"{dst_dir}/INEGI_Logotipo_5.jpg")
			bati = [f for f in files if f.endswith(".tif")]
			bati = bati[0] if len(bati)>0 else None
			gdb2gpkg(gdb,gpk,bati,f"{root}/{bati}")
			os.system(f'{dst_dir}/{ent}.qgz')
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


