import os
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
	
	def poligonos_enPartes(self):
		from .poligono_enPartes import inicio_pP
		return inicio_pP

	def lineaCentral(self):                                                                                                                                                      
		from .generalizacion.lineaCentral import inicio_lc
		return inicio_lc
	def datosGenerales(self):
		from .generalizacion.datosGenerales import inicio
		return inicio


