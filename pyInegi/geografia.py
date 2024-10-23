def generalizar(func=""):
	from .reducePuntos import reducePuntos
	from .separaLineas import separaLineas
	obj = {"reducePuntos":reducePuntos,"separaLineas":separaLineas}
	return obj[func]
