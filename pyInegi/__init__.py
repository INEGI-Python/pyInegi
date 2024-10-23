import generalizar as gen

class Generalizar:
    def reducePuntos(**_d):
        gen.reducePuntos(gdb=_d.gdb, feat=_d.feat, camp=_d.camp.split(","),dist=_d.dist,ver=_d.ver)
    def separaLineas(_gdb,_fCls,distancia,cpu=cpu_count(),vtx=0,eps=0.001,apx=0.02):
        gen.separaLineas(*[_gdb,_fCls,distancia,cpu,vtx,eps,apx])

__version__="1.0.0"
__ALL__ = ["generalizar","basico","reducePuntos","separaLineas"]
