def generalizar(func=""):
	def _reduceP():
		from .reducePuntos import inicio_rp
		return inicio_rp
	def _separaL():
		from .separaLineas import inicio_sl
		return inicio_sl
	obj = {"reducePuntos":_reduceP(),"separaLineas":_separaL(),"ayuda":"Aqui va algunas presiciones del uso de esta libreria","desc":"Esta libreria fue desarrollada por el departamento de Generalización adscrito a la subdireccion de Edición Digital del INEGI. CopyRight INEGI@2024"}
	return obj[func]