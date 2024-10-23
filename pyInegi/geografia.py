def generalizar(func=""):
	from .reducePuntos import inicio_rp
	from .separaLineas import inicio_sl
	obj = {"reducePuntos":inicio_rp,"separaLineas":inicio_sl}
	return obj[func]