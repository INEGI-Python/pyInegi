import pyInegi

f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
#print(f.datosGenerales()(tipo="descripcion",res='json',mayusculas=True))
f.run(gdb='pyInegi/datos/prueba1.shp', feat='_', camp=["*"],dist=2,ver=2)


