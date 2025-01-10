ACERCA DE
=====

Esta libreria fue creada por el Instituto Nacional de Estadisticas y Geografia


Instalación
=====

			pip install  git+https://github.com/INEGI-Python/pyInegi.git

USO
=====

 pyInegi
 
  	generalizacion
  
            <b>lineaCentral(file=str,dist=int,cpu=int,web=int,rows=int)  -> String</b>
                    file: Ruta relativa o absoluta de la ubicacion de la fuente de datos (Polígonos). Tambien acepta URL.
                    dist: Distancia en metros minima que debera tener entre vertice y vertice en los poligonos. 
                    cpu: Cantidad de unidades logicas de procesamiento a utilizar de manera paralela. 
                    web: Indica si al final del procesamiento, el sistema muestra el resultado de sobre un sitio web local.
                    rows: Cantidad de registros o poligonos a procesar.
        	Ejemplo:

                	file_result = pyInegi.generalizacion.lineaCentral(file="carpeta/archivo.shp",dist=10,cpu=8,web=1,rows=-1)

            reducePuntos(gdb)           
===

	pyInegi --help
