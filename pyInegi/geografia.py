def generalizar(func="ayuda"):
#####       T a r e a      1   
#####       T a r e a      2
	def _separaL():
		from .separaLineas import inicio_sl
		return inicio_sl

#####       T a r e a      3	
	def _puertos():
		from .instalacionesPortuarias import inicio_ip
		return inicio_ip
#####       T a r e a      4
	def _quitaVertices():
		from .quitaVertices import  inicio_qV
		return inicio_qV
#####       T a r e a      5
	def _reduceP():
		from .reducePuntos import inicio_rp
		return inicio_rp

#####       T a r e a      6
	def _lineaC():                                                                                                                                                      
		from .lineaCentral import inicio_lc
		return inicio_lc
	def desc():
		return """pyInegi en su modulo generalizar fue desarrollado por el departamento de Generalización del Instituto Nacional de Estadisitica y Geografia. CopyRight   INEGI@2024 """
	def ayuda():
		return """ Aqui va la super ayuda de como usar la libreria 
usar las lineas que le sean posibles"""


	return eval({"reducePuntos":"_reduceP","separaLineas":"_separaL","lineaCentral":"_lineaC",
    "ayuda":"ayuda","desc":"desc"}[func])()
