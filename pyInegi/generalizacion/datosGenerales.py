
def formato(msj, res, may=False):
	a = msj.upper() if may else msj
	return {"sucesses":True,"message":a} if res=="json" else a

def ayuda(_dat):
	a = """ Aqui va la super ayuda de como usar la libreria usar las lineas que le sean posibles"""
	print(list(_dat.values())[1:])
	return formato(a,*list(_dat.values())[1:])

def descripcion(_dat):
	a ="""pyInegi es una libreria de código abierto para PYTHON desarrollada por el Instituto Nacional de Estadísitica y Geografía. INEGI. La cual cuadyuba a los ciudadanos mexicanos asi como al resto del mundo y sus alrededores a el proceda  CopyRight   INEGI@2024 """
	print(list(_dat.values())[1:])
	return formato(a,*list(_dat.values())[1:])

def inicio(**datos):
    return eval(f"{datos['tipo']}({datos})")