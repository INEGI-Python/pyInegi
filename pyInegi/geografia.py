class Generalizar(object):
	def __init__(self,**obj):
		self.param=obj
		self.idioma=obj['idioma']
		self.run = eval(f"self.{obj['func']}")()
	def separaLineas(self):
		from .separaLineas import inicio_sl
		inicio_sl(self.param.values())
	def instalacionesPortuarias(self):
		from .instalacionesPortuarias import inicio_ip
		return inicio_ip
	def quitaVertices(self):
		from .quitaVertices import  inicio_qV
		return inicio_qV
	def reducePuntos(self):
		from .reducePuntos import inicio_rp
		inicio_rp(self.param)
	def lineaCentral(self):                                                                                                                                                      
		from .lineaCentral import inicio_lc
		return inicio_lc
	def poligonos_enPartes(self):
		from .poligono_enPartes import inicio_pP
		return inicio_pP
	def desc(self):
		return """pyInegi en su modulo generalizar fue desarrollado por el departamento de Generalización del Instituto Nacional de Estadisitica y Geografia. CopyRight   INEGI@2024 """
	def ayuda(self,_dat):
		a = """ Aqui va la super ayuda de como usar la libreria usar las lineas que le sean posibles"""                     
		a1 = upper(a) if _dat["mayusculas"] else a
		a2 = {"sucesses":True,"message":a1} if _dat['tipoRes']=="json" else a1 
		return a2	 
		
			




# def func(f):
# 	eval("from .{} import inicio".format(f))
# 	return inicio

# mapasWeb  = {}
# d={"multiprocesos":"func1","lib2":"func2","lib3":"func3"}
# for k in d.keys():
# 	mapasWeb[d[k]]=f"func({k})"

# from ctypes import Structure,c_
# class Generalizar(Structure):
# 	_fields_=[('multiproceso',)]
# 	def __init__(self):
# 		self.multiproceso = "multiproceso"
# 		self.reducePuntos = ".reducePuntos"
# 	def run(s):
# 		eval("from %s import inicio" % s.multiproceso)
	