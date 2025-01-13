import pyInegi
pyInegi.ayuda()


#pyInegi.generalizacion.reducePuntos.inicio_rp(gdb='datos/prueba_reducePuntos.shp', feat='_', camp="Jerarquia:1,geografico:1,num_hab:0".split(","),dist=5500,ver=1)
#pyInegi.generalizacion.quitaVertices.inicio_gpd(shp1="DatosEntrada/pol1.shp",shp2="DatosEntrada/vtx1.shp")
pyInegi.generalizacion.webMap.WebMAP(datos=["DatosSalida/resQuitaVtx_4.shp"],tipos=["POLYGON"],names=["Layer"],color=["red"])


#if __name__ == "__main__":
#    pIg.lineaCentral.inicio(idioma="es",file="DatosEntrada/prueba3.shp",dist=10,cpu=16,web=1,rows=25)
