def generalizar(func="ayuda"):
	def ayuda():
		return """ Aqui va la super ayuda de como usar la libreria 
usar las lineas que le sean posibles"""
	def desc():
		return """pyInegi en su modulo generalizar fue desarrollado por el departamento de Generalización del Instituto Nacional de Estadisitica y Geografia. CopyRight   INEGI@2024 """
	def _reduceP():
		from .reducePuntos import inicio_rp
		return inicio_rp
	def _separaL():
		from .separaLineas import inicio_sl
		return inicio_sl
	def _lineaC():                                                                                                                                                      
		from .lineaCentral import inicio_lc
		return inicio_lc

	def _eliminaVtxEsp():
		from .eliminaVtxEsp import inicio_ev
		return inicio_ev

	def _puertos():
		from .instalacionesPortuarias import inicio_ip
		return inicio_ip


	obj = {"reducePuntos":"_reduceP","separaLineas":"_separaL","lineaCentral":"_lineaC","puertos":"_puertos",
    "ayuda":"ayuda","desc":"desc"}
	return eval(obj[func])()