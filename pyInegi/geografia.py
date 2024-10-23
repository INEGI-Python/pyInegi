def generalizar(func=""):
	import reducePuntos
	import separaLineas
	obj = {"reducePuntos":reducePuntos.inicio,"separaLineas":separaLineas.inicio}
	return obj[func]
