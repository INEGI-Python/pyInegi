
from time import localtime as  lc,time as t
from arcpy import SpatialReference as sPt, Point as pt, Geometry as _aG, Array as aa
from os import path
import numpy as np
import matplotlib.pyplot as plt
from  arcpy import env
from arcpy.da import  SearchCursor as sC
#from multiprocessing import cpu_count,Pool
import argparse,gc


def _angles_(a, inside, in_deg):  
	def _x_(a):	   
		ba = a - np.concatenate((a[-1, None], a[:-1]), axis=0)
		bc = a - np.concatenate((a[1:], a[0, None]), axis=0)
		return np.cross(ba, bc), ba, bc 
	cr, ba, bc = _x_(a)
	dt = np.einsum('ij,ij->i', ba, bc)	
	ang = np.arctan2(cr, dt) 
	TwoPI = np.pi * 2
	if inside:
		angles = np.where(ang < 0, ang + TwoPI, ang)
	else:
		angles = np.where(ang > 0, TwoPI - ang, ang)
	if in_deg:
		angles = np.degrees(angles)
	return angles

def crearShape(datos,outshp,loc,tipo="POLYGON"):
	from arcpy.da import  InsertCursor as iC
	from arcpy.management import CreateFeatureclass as cFc, AddField as aF
	cFc(loc,outshp,tipo,None,"DISABLED","DISABLED",sPt(6372))
	with iC(outshp,["OID@","SHAPE@"]) as inserCur:
		for k in list(datos.keys()):
			_dat = _aG(tipo.lower(),aa([pt(p.X,p.Y) for p in datos[k]]))
			inserCur.insertRow([k,_dat])

def shift_point(c1, c2, offset):
    try:
        x1, y1 = c1
        x2, y2 = c2
    except:
        print(c1, c2)
    if ((x1-x2) == 0) and ((y1-y2) == 0):  # zero length line
        x_new, y_new = x1, y1
    else:
        rel_length = np.minimum(offset/np.sqrt((x1-x2)**2+(y1-y2)**2), 1)
        x_new = x1 + (x2-x1)*rel_length
        y_new = y1 + (y2-y1)*rel_length
    return pt(x_new, y_new)

def extend_line(line, crece, side='both'):
	if side == 'both':
		sides = ['start', 'end']
	else:
		sides = [side]
	largo = line.tam
	coo = line.coords
	offset =  (crece - largo)/2
	for side in sides:	
		if side == 'start':
			p_new = shift_point(coo[0], coo[1], -1. * offset)
			lineaNew = [(p_new.X,p_new.Y)] + coo[:]
		elif side == 'end':
			p_new = shift_point(coo[-1], coo[-2], -1. * offset)
			lineaNew = coo[:] + [(p_new.X,p_new.Y)]
	return lineaNew

def medio(p1,p2):
	return ((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)
def distancia(p1,p2):
	return ((p2.X-p1.X)**2  + (p2.Y-p1.Y)**2)**0.5
def importDatos(feat,campos,donde,dens=False):
	dct_tmp = {}
	for c in sC(feat,campos,donde):
		newCoo = [[[]]] if dens else c[1].__geo_interface__["coordinates"]
		if dens:
			coo = c[1].__geo_interface__["coordinates"][0]
			for i in range(len(coo)-1):
				newCoo[0][0].append(coo[i])
				m = medio(coo[i],coo[i+1])
				newCoo[0][0].append(m)
			newCoo[0][0].append(coo[-1])
		if dct_tmp.get(c[0]):
			dct_tmp[c[0]].append({"id":c[0],"geom":newCoo,"tam":c[2]})
		else: 
			dct_tmp[c[0]]=[{"id":c[0],"geom":newCoo,"tam":c[2]}]
	return dct_tmp

def closest_object(geometries, point):
	min_dist, min_index = min((distancia(point,geom), k) for (k, geom) in enumerate(geometries))
	return geometries[min_index], {"dist": min_dist,"coo":point},min_index

def run(polygono,linea,_off,prev,dens):
	t1 = t()
	coorPoly = polygono["geom"][0][0] if dens else polygono["geom"][0]
	x,y=[],[]
	for c in coorPoly:
		x.append(c[0])
		y.append(c[1])
	plt.plot(x,y,linewidth=1)
	plt.plot(x,y,"ro",linewidth=1)
	plt.annotate(polygono["id"], xy=(x[0], y[0]), xytext=(x[0],y[0]),arrowprops=dict(facecolor='green', shrink=0.05),annotation_clip=True)
	class Linea:
		def __init__(self,coords):
			self.coords =coords["geom"][0]
			self.tam = coords["tam"]
			self.x,self.y = [],[]
			self.nX,self.nY=[],[]
			self.pX,self.pY=[],[]
			self.nC = None
			self.startEndPos=None
		def dibuja(s,plt):
			for c in s.coords:
				s.x.append(c[0])
				s.y.append(c[1])
			plt.plot(s.x,s.y,linestyle="solid", linewidth=1)
		def dibujaNew(s,plt):
			for n in s.nC:
				s.nX.append(n[0])
				s.nY.append(n[1])
				plt.plot(s.nX,s.nY,linestyle=":",linewidth=1)
	


	geomPoli = [pt(*c) for c in coorPoly]
	start_end=[]
	lineas = [Linea(coorOri) for coorOri in linea]
	for (k,l) in enumerate(lineas):
		l.dibuja(plt)
		l.nC = extend_line(l,_off)
		l.dibujaNew(plt)
		start_end.append(pt(*l.nC[0]))
		start_end.append(pt(*l.nC[-1]))
		l.startEndPos=k*2
	newPoly=[]
	numP=len(geomPoli)
	for k in range(numP):
		_g,_d,_i = closest_object(start_end,geomPoli[k])
		_ta = [l.tam for l in lineas if l.startEndPos==_i or l.startEndPos+1 ==_i]
		_d_ = ((_off-_ta[0])/2)*1.5
		if _d["dist"]<=_d_ and k>0:
			arr= geomPoli[k-1:k+2]
			_ang = _angles_(np.array([(a.X,a.Y) for a in arr]),True,True)[1]
			if  _ang<260  or _ang>280:
				newPoly.append(_g)
		else:
			newPoly.append( _d["coo"])

	newPoly.append(geomPoli[-1])	
	print("[%d] Proceso Finalizado. Tiempo: %.3f seg" % (polygono["id"],t()-t1))
	if prev:
		nXp = [n.X for n in newPoly]
		nYp = [n.Y for n in newPoly]
		plt.plot(nXp,nYp,linestyle="solid",linewidth=3)
		plt.title("Poligono %d" % polygono["id"])
		plt.show()
	#del line
	#gc.collect()
	return newPoly



def inicio_ip(poly,lineas,offset,min,max, cpu,dens,prev,_gdb):
	t0=t()
	l=list(lc())
	print("[%s]  Iniciando procedimiento." % str(l[3:6])[1:-1].replace(", ",":"))
	print("[info]  Leyendo datos....")
	env.workspace = path.abspath("")  if _gdb is None else _gdb
	env.overwriteOutput = True
	_poly,_line=[],[]
	dct_poly = importDatos(poly,["tmp","SHAPE@","SHAPE@AREA","promedio"],"promedio >= %d And promedio <= %d" %(min,max),bool(dens))
	dct_line = importDatos(lineas,["tmp","SHAPE@","SHAPE@LENGTH"],"")
	res=[]
	for i in list(dct_poly.keys()):
		_poly.append(dct_poly[i][0])
		_line.append(dct_line[i])
		res.append(run(dct_poly[i][0],dct_line[i],offset,bool(prev),bool(dens)))
	crearShape(dict(enumerate(res)),"RESULTADO.shp",path.abspath(""))


	# with Pool(cpu) as pool:
	# 	res = pool.starmap(run,zip(_poly,_line,[offset for x in range(len(_poly))],[bool(prev) for x in range(len(_poly))]))
	# 	pool.close()
	# 	crearShape(dict(enumerate(res)),"RESULTADO.shp")
	tt=t()-t0
	return tt

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Ajusta a las medidas minimas las intalaciones portuarias")
	parser.add_argument('PORT',type=str,  help="Ruta absoluta o relativa a la GDB donde se encuentra el FeatureClass o ruta del ShapeFile de las instalaciones porturarias (Poligono)")
	parser.add_argument('TRANS', type=str,  help="Ruta absoluta o relativa a la GDB donde se encuentra el FeatureClass o el ShapeFile de las lineas Transects")
	parser.add_argument('DIST',type=int, nargs='?', default=10, help="Dimencion minima del ancho en metros que debe de tener una instalacion porturaria. DEFAULT: 10 ")
	parser.add_argument('MIN',type=int, nargs='?', default=40, help="Porcentaje minimo de cobertura de lineas en el poligono que no cumple la distancia. DEFAULT: 40 ")
	parser.add_argument('MAX',type=int, nargs='?', default=60, help="Porcentaje maximo de cobertura de lineas en el poligono que no cumple la distancia. DEFAULT: 60 ")
	parser.add_argument('CPU',type=int, nargs='?', default=2, help="Numero de procesos u objetos que se ejecutaran en paralelo en un tiempo dado. DEFAULT: 2")
	parser.add_argument('DENS',type=bool, nargs='?', default=False, help="Densificar Poligonos con un vertice en medio de dos vertices. DEFAULT: False ")
	parser.add_argument('PREV',type=bool, nargs='?', default=False, help="Ver vista previa de los poligonos resultantes. DEFAULT: False ")
	parser.add_argument('GDB',type=str,  nargs='?', default=None, help="Ruta absluta o relativa de la geodabase. DEFAULT: Nulo")
	a = parser.parse_args()
	print(a)
	tiempo=inicio_ip(a.PORT,a.TRANS,a.DIST,a.MIN,a.MAX,a.CPU,a.DENS,a.PREV,a.GDB)
	print("Tiempo Total: %.2f segundos" % tiempo)
	print('Ruta Resultado:"%s/RESULTADO.shp"' % path.abspath(""))

	# %pro% principal.py datos/InstalacionPortuaria.shp datos/Transect.shp 10 45 55 8 True True geodatabase.gdb
	#%_py% principal.py datos/InstalacionPortuaria.shp datos/Transect.shp