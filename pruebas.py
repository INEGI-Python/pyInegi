import pyInegi

f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
f.run(gdb='pyInegi/datos/prueba1.shp', feat='_', camp=["*"],dist=1,ver=1)
