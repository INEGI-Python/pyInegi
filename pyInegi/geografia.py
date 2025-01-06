import os
class Generalizar(object):
	def __init__(self,**argu):
		self.a = argu
	def acerca(self):
		return type(self).__name__
	def run(self,metodo):
		def lc():
			from .generalizacion.lineaCentral  import inicio
			return inicio
		def sp():
			from .generalizacion.separaLineas  import inicio
			return inicio
		def dg():
			from .generalizacion.datosGenerales  import inicio
			return inicio
		sw = {"lineaCentral": lc(),"separaLineas":sp(),"datosGenerales":dg()}
		return sw[metodo](self.a)
class lineaCentral(Generalizar):
    pass
class separaLineas(Generalizar):
    pass
class datosGenerales(Generalizar):
    pass


	# def separaLineas(self):
	# 	from .separaLineas import inicio_sl
	# 	inicio_sl(self.param.values())
	# def instalacionesPortuarias(self):
	# 	from .instalacionesPortuarias import inicio_ip
	# 	return inicio_ip
	# def quitaVertices(self):
	# 	from .quitaVertices import  inicio_qV
	# 	return inicio_qV
	# def reducePuntos(self):
	# 	from .reducePuntos import inicio_rp
	# 	inicio_rp(self.param)
	
	# def poligonos_enPartes(self):
	# 	from .poligono_enPartes import inicio_pP
	# 	return inicio_pP

	# def datosGenerales(self):
	# 	from .generalizacion.datosGenerales import inicio
	# 	return inicio


