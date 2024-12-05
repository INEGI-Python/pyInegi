
def ayuda(_dat):
	a = """ Aqui va la super ayuda de como usar la libreria usar las lineas que le sean posibles"""                     
	a1 = upper(a) if _dat["mayusculas"] else a
	a2 = {"sucesses":True,"message":a1} if _dat['res']=="json" else a1 
	return a2

def inicio(datos):
    return eval(f"{datos['tipo']}")(datos)