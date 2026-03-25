import requests, argparse
import zipfile
import io
from pyInegi import  generalizacion as gen
import os

def estilo(colores):
	return [dict(fillColor=c.split("-")[0],color=c.split("-")[1]) for c in colores]


def descargar_y_extraer_zip(_dat):
    # Descargar el archivo ZIP desde la URL
    response = requests.get(datos(_dat.c))
    response.raise_for_status()  # Verificar si la descarga fue exitosa

    # Extraer el contenido del archivo ZIP
    os.makedirs(_dat.d, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(_dat.d)

def datos(capa="lista"):
    obj = {"RNC2024": "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/caminos/2024/794551132166_s.zip",
           "RNC2025": "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/caminos/2025/794551163030_gpk.zip"}
    if capa=="lista":
        return obj.keys()    
    else:
        url = obj.get(capa,False)
        if not url:
             print(f"El nombre de la capa {capa} no existe")
             exit(0)
        else:
             return url

if __name__=="__main__":
    args = argparse.ArgumentParser(description="Metodo para descargar capas  de  informacion de INEGI",epilog="Sabe para que sea este")
    args.add_argument("--l",type=str,default=None,help="Muestra la lista  de  capas disponibles")
    args.add_argument("--c",type=str,default=None,help="Nombre de la capa  de informacion a descargar")
    args.add_argument("--d",type=str,default="",help="Ruta absoluta o relativa de la carpeta donde se guardara la descarga. Si la carpeta  no existe la crea.")
    args = args.parse_args()
    if args.l=="lista":
         for i,v in enumerate(list(datos())):
              print(f"{i+1} - {v}")
    else:
        descargar_y_extraer_zip(args)
        #gen.webMap.WebMAP(datos=[(f"{args.d}/conjunto_de_datos/rnc2025.gpkg","red_vial"),(f"DatosEntrada/manzanas_cdmx.shp",None)], tipos=["LINESTRING","POLYGON"], names=["Red Vial","Naranjas"],estilo=[dict(fillColor="red",color="red"),dict(fillColor="black",color="gray") ],web=1,rows=100000)

#####    4189     1433    3898   5602 