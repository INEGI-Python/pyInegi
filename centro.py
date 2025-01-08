import httpimport
with httpimport.remote_repo('https://github.com/INEGI-Python/pyInegi.git'):
	from pyInegi.generalizacion import lineaCentral as lc
	if __name__=="__main__":
		lc.inicio(file="DatosEntrada/SinIslas.shp",dist=8,cpu=16,web=1,rows=-1)
