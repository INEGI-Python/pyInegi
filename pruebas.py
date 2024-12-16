import os
from time import time as t
import geopandas,shapely
import numpy as np
from multiprocessing import Pool
from pyInegi.generalizacion import lineaCentral

#sal = open()

def multi(g,pol):
    print(f"[info] Proceso PID: {os.getpid()} ...",end="")
    ini=t()
    a = lineaCentral.Centro(g,3)
    tmp = a.createCenterline()
    geoms = shapely.MultiLineString([shapely.LineString(t.__geo_interface__["coordinates"]) for t in tmp])
    del a
    print(f"..... {t()-ini}")
    return {"pol":pol, "geometry":geoms.simplify(0.5)}


if __name__ == "__main__":
    x =  geopandas.read_file("prueba3.shp",rows=3)
    id_pol=x.loc[:,"OBJECTID"]
    CRS = x.crs.to_string()
    x.plot()
    with Pool(4) as pool:
        dat = pool.starmap(multi,zip(x.geometry,id_pol))
        
        print(dat)
        _d = geopandas.GeoDataFrame(data=dat,crs=CRS)
        _d.to_file("DatosSalida/centerSalida.shp")
    
    
        
        
        
# import pyInegi

# f = pyInegi.Generalizar(idioma="es", func="lineaCentral")
# f.run(gdb='MOPIGMA.gdb', feat='prueba2', camp=["*"],dist=15,ver=1)

