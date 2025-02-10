import requests
import zipfile
import io
from pyInegi.generalizacion import webMap

def descargar_y_extraer_zip(url, destino):
    # Descargar el archivo ZIP desde la URL
    response = requests.get(url)
    response.raise_for_status()  # Verificar si la descarga fue exitosa

    # Extraer el contenido del archivo ZIP
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(destino)

# Ejemplo de uso
url = "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/caminos/2024/794551132166_s.zip"
destino = "DatosEntrada"
#descargar_y_extraer_zip(url, destino)
webMap.WebMAP(datos=["DatosEntrada/conjunto_de_datos/red_vial.shp"], tipos=["LINESTRING"], names=["Red Vial"],color=["Red"],web=1,rows=500000)