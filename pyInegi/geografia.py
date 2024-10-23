def generalizar(func=""):
	import reducePuntos
	import separaLineas
	obj = {"reducePuntos":reducePuntos,"separaLineas":separaLineas}
	return obj[func]
