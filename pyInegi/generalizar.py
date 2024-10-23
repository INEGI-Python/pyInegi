from .reducePuntos import reducePuntos
from .separaLineas import separaLineas
from .clase1.basico import *

class Generalizar:
    def reducePuntos(**_d):
        reducePuntos(gdb=_d.gdb, feat=_d.feat, camp=_d.camp.split(","),dist=_d.dist,ver=_d.ver)
    def separaLineas(_gdb,_fCls,distancia,cpu=cpu_count(),vtx=0,eps=0.001,apx=0.02):
        separaLineas(*[_gdb,_fCls,distancia,cpu,vtx,eps,apx])



print(punto(5,9))