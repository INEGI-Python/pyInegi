#import pyInegi
#if __name__ == "__main__":
#   pyInegi.generalizacion.lineacentral_sinhuecos.LineaCentral_SinHuecos(file="DatosEntrada/SinIslas.shp",dist=1,simp=3,suavi=3,cpu=16,web=0,rows=-1)


#pyInegi.ayuda()


#pyInegi.generalizacion.reducePuntos.inicio_rp(gdb='datos/prueba_reducePuntos.shp', feat='_', camp="Jerarquia:1,geografico:1,num_hab:0".split(","),dist=5500,ver=1)
#pyInegi.generalizacion.quitaVertices.QuitaVertices(shp1="DatosEntrada/pol1.shp",shp2="DatosEntrada/vtx1.shp")
#pyInegi.generalizacion.webMap.WebMAP(datos=["DatosSalida/resQuitaVtx.shp"],tipos=["POLYGON"],names=["Layer"],color=["red"])



import httpimport

with httpimport.remote_repo("https://github.com/INEGI-Python/pyInegi.git"):
	import pyInegi
	pyInegi.ayuda()
	

