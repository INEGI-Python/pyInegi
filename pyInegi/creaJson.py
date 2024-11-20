import json
import numpy as np
import geopandas as pan
import  matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show

ima = rasterio.open("dados/orographic.tif")
metodos = dir(ima)
base = ima.read.__class__
for m in metodos:
	tmp=eval(f"ima.{m}.__class__")
	print(tmp)
	try:
		x = f"ima.{m}()"  if base==tmp else f"ima.{m}"
		print(eval(x))
	except Exception as e:
		print(f" *-*-*-*-*-*-*-*-*-*-*-*      {e}      *-*-*-*-*-*-*-*-*-*-*- ")
fig,ax = plt.subplots()

#extent=[ima.bounds[0],ima.bounds[2],ima.bounds[1],ima.bounds[3]]
#print(extent)
extent=[ima.bounds[0],ima.bounds[2],ima.bounds[1],ima.bounds[3]]
print(ax.get_clip_box())
ax = show(ima,extent=extent,ax=ax, cmap="Set1")

plt.plot(ax=ax)

# keys = ["id",				"anio","mes","apellido_paterno","apellido_materno","nombre","tno_cve","nombramiento","sexo","sheldon_issste","mult_sdo_issste",	"fecha_alta",					"fecha_ingreso",		"antig",	"num_ramo",		"ramo",																														"entidad",				"mod_cve",							"modalidad",																"sector"]
# f = open("2024_10_3_DURANGO.txt","r")
# _dat=[]
# for r in f:
# 	if len(r.split(',')[:20])==len(keys):
# 		_dat.append(r.split(',')[:20])
# 	else:
# 		print(r)


# dF = pan.DataFrame(data=_dat,columns=keys)
# dF.set_index("nombre")
# print(dF.query("nombre=='MELISSA' and  apellido_paterno == 'MERCADO'"))


#f.close()





