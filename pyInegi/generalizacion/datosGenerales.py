
def formato(msj, res="", may=False):
	a = msj.upper() if may else msj
	return {"sucesses":True,"message":a} if res=="json" else a

def ayuda(**_dat):
	_dat['a'] = """ Aqui va la super ayuda de como usar la libreria usar las lineas que le sean posibles"""
	return formato(*list(_dat.values()))

def descripcion(**_dat):
	_dat['a'] ="""pyInegi es una libreria de código abierto para PYTHON desarrollada por el Instituto Nacional 
	de Estadísitica y Geografía. INEGI. La cual cuadyuba a los ciudadanos mexicanos asi como al resto 
	del mundo y sus alrededores o de donde proceda.  CopyRight   INEGI@2024 """
	return formato(*list(_dat.values()))




