def generalizar(func=""):
	from . import reducePuntos
	from . import separaLineas
	obj = {"reducePuntos":reducePuntos.inicio,"separaLineas":separaLineas.inicio}
	return obj[func]
