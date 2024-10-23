import numpy as  np
import json
from time import localtime as   lc,time as t


def getGeom2Feat(ent):
	from arcpy.da import SearchCursor as sC
	obj={}
	with sC(ent,["OID@","SHAPE@"]) as cur:
		for row in cur:
			obj[row[0]]=row[1].__geo_interface__['coordinates']
		return obj
	
def crearFeat(dSet,nom,_dat,_key,_tip,_proc,campo):
	from arcpy.da import  InsertCursor as iC
	from arcpy.management import CreateFeatureclass as cFc, AddField as aF
	from arcpy import SpatialReference as sPt, Point as pt, Geometry as _aG, Array as aa
	id=1
	_file = '%s%s' % (nom,_proc)
	cFc(dSet,_file,_tip,None,"DISABLED","DISABLED",sPt(6372))
	aF("tmp/%s"%_file,campo,"SHORT")
	with iC("tmp/%s" %_file,["SHAPE@","OID@",campo]) as i:
		for _k in _key:
			_datTmp = [_dat[_k]['coord']] if _tip=='POLYGON' else _dat[_k]
			for _d in _datTmp:
				_gL_ = _aG(_tip.lower(),aa([pt(*p) for p in _d]))			
				i.insertRow([_gL_,id, _k])
				id+=1
	return _file

def getPend(p1,p2):
	try:
		return (p2[0]-p1[0])/(p2[1]-p1[1])
	except Exception as e:
		print(p1,p2)
		return 0

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

def unir(_linCen,_j):
	for _i in range(len(_j)):
		if _linCen[0]==_j[_i] or _linCen[1]==_j[_i]:
			if _linCen[0]==_j[_i]:
				_linCen.reverse()
			_vtN = _j[_i+1]  if _i%2 == 0  else _j[_i-1]
			_linCen.append(_vtN)
			arr = np.asarray(_linCen)
			if len(arr)>2:
				_ang = _angles_(arr,inside=True,in_deg=True)
				return _linCen if 240<_ang[1]<297 or 75<_ang[1]<105 else False
	return False
		
	
	
	

def avance(x):
	v=''
	a=open("avance.aux","+r")
	while v=='':
		v = a.read()
		a.seek(0)
	porc = float(v)+x
	a.write(str(porc))
	a.truncate(5)
	a.close()
	return porc

def getCampo(_cam):
	a=open("avance.json","r")
	_obj = json.loads(a.read())
	a.close()
	return _obj[_cam]

def textFile(_arch,_modo,_dato=None):
	a = open(_arch,_modo) 
	r = a.write(_dato) if _modo in ["+a","w"] else a.read()
	a.close()
	return r

def putAtention(id):
	a = open("control.json","r")
	o = json.loads(a.read())
	a.close()
	tiempo = None
	if o.get(id).get("local") is None:
		o[id]={"time":t(),"local":[str(list(lc())[3:6]).replace(",",":")[1:-1]]}
		tiempo = o.get(id).get("local")[0]
	else:
		tiempo = t() - o.pop(id).get("time")
		#o[id]["local"].append(str(list(lc())[3:6]).replace(",",":")[1:-1])
	a = open("control.json","w")
	a.write(json.dumps(o,indent=4))
	a.close()
	return tiempo
	
def separar(_datos,_rutas,uC,sC,_aG,aa,pt):
		def outLine(_ar):
			return (False if _ar['y'][0] < _ar['y'][1] < _ar['y'][2] or _ar['y'][0] >_ar['y'][1] > _ar['y'][2]  else True )  if _ar['x'][0] == _ar['x'][1] == _ar['x'][2] else (False if _ar['x'][0] < _ar['x'][1] < _ar['x'][2] or _ar['x'][0] > _ar['x'][1] > _ar['x'][2] else True)
		bloques, ban =[],False
		with uC("tmp/resultado",["id_tmp","SHAPE@"]) as res:
			for row in res:
				_pol = _datos['geomEnt'][row[0]]['coord']
				_lin = [{"id":n[0],"_coo": n[1].__geo_interface__['coordinates'][0],"nP":n[2]} for n in sC("tmp/%s" %_rutas['_nom_l'],["OID@","SHAPE@","numPol"],where_clause="numPol = %d" % row[0])]
				aMover={"ori":[],"nuevo":[]}
				if len(_lin)>0:	
					for l in _lin:
						x1,y1 = l['_coo'][0][0],l['_coo'][0][1]
						x2,y2 = l['_coo'][1][0],l['_coo'][1][1]
						xd,yd = (x1,y1) if (x1,y1) in _pol else (x2,y2)
						v1,v2 = x2-x1,y2-y1
						xmas= xd+ _datos['distancia']
						ymas = ((v2*xmas) -(v2*x1)+(v1*y1))/v1
						#xmen= xd-_s.getDist()
						#ymen = ((v2*xmen) -(v2*x1)+(v1*y1))/v1
						dist = ((xd-xmas)**2+(yd-ymas)**2)**0.5
						_obj={ }
						prop=dist/(_datos['distancia']/2)
						dis1 = [(yd-ymas)/prop,_datos['distancia']/prop]
						_pos = [ xd+dis1[1] , yd-dis1[0]]
						_obj["x"],_obj["y"]=[x1,_pos[0],x2],[y1,_pos[1],y2]
						_pos =_pos if outLine(_obj) else [ xd-dis1[1] , yd+dis1[0]]
						aMover["ori"].append(tuple([xd,yd]))
						aMover["nuevo"].append(tuple(_pos))	
					for i in range(len(_pol)):
						if _pol[i] in aMover["ori"]:
							index =  aMover["ori"].index(_pol[i])
							_pol[i]=aMover["nuevo"][index]
							if not ban:
								bloques.append({"ini":i,"fin":None})
								ban=True
							else:
								pass
						elif ban:
							bloques[-1]["fin"]=i-1
							ban=False
					if len(bloques)>0:
						if bloques[-1]["fin"] == None:
							bloques.pop()
						bloques.reverse()
						for b in bloques:
							for i in range(b["fin"]+_datos['vtx'],b["fin"],-1):
								try:
									_pol.pop(i)
								except Exception as e:
									pass
							for i in range(b["ini"]-1,b["ini"]-_datos['vtx']-1,-1):
								try:
									_pol.pop(i)
								except Exception as e:
									pass
					try:
						_g_=aa([pt(*p) for p in _pol])
						row[1]= _aG("polygon",_g_)
						res.updateRow(row)
					except:
						print(_pol)
		return  len(bloques)