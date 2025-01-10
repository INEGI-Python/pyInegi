from .basico import funciones
from .generalizacion import lineaCentral,reducePuntos,webMap
import webbrowser
__version__="1.0.0"
__ALL__ = ["generalizacion","ayuda","descripcion","reducePuntos","lineaCentral","webMap","basico"]



def formato(msj, res="", may=False):
	a = msj.upper() if may else msj
	return {"sucesses":True,"message":a} if res=="json" else a

def ayuda():
    webbrowser.open_new("https://github.com/INEGI-Python/pyInegi/tree/main")

def descripcion(**_dat):
	_dat['a'] ="""pyInegi es una libreria de código abierto para PYTHON desarrollada por el Instituto Nacional 
	de Estadísitica y Geografía. INEGI. La cual cuadyuba a los ciudadanos mexicanos asi como al resto 
	del mundo y sus alrededores o de donde proceda.  CopyRight   INEGI@2024 """
	return formato(*list(_dat.values()))

