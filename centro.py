import httpimport
with httpimport.remote_repo('https://github.com/INEGI-Python/pyInegi.git'):
	from pyInegi.generalizacion import lineaCentral as lc
	lc.inicio(file="DatosEntrada/prueba3.shp",dist=8,cpu=16,web=1,rows=20)
