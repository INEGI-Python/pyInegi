
from folium import Polygon
import rtree,json
from shapely import GeometryCollection, LineString, MultiLineString, MultiPoint, MultiPolygon, Point
import numpy as np


def shift_point(c1, c2, offset):
    """
    shift points with offset in orientation of line c1->c2
    """
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
    return Point(x_new, y_new)

def extend_line(line, offset, side='both'):
    """extend line in same orientation"""
    if side == 'both':
        sides = ['start', 'end']
    else:
        sides = [side]

    for side in sides:
        coords = line.coords
        if side == 'start':

            p_new = shift_point(coords[0], coords[1], -1. * offset)
            line = LineString([p_new] + coords[:])
        elif side == 'end':
            p_new = shift_point(coords[-1], coords[-2], -1. * offset)
            line = LineString(coords[:] + [p_new])
    return line

def interseccion(ids1, lines1, lines2=None, tolerance=0., min_spacing=0):
    ids = []
    tree_idx_pnt = rtree.index.Index()
    ipnt = 0
    if lines2 is None:
        # build spatial index for lines1
        tree_idx = rtree.index.Index()
        lines_bbox = [l.bounds for l in lines1]
        for i, bbox in enumerate(lines_bbox):
            tree_idx.insert(i, bbox)

    
    # create multilinestring of close-by lines
    for i1, l1 in zip(ids1,lines1):
        l1 = l1[0]
        if lines2 is None:
            # find close-by lines based on bounds with spatial index
            hits = list(tree_idx.intersection(lines_bbox[i1]))
            lines_hit = MultiLineString([lines1[i] for i in hits if i != i1])
        else:
            if isinstance(lines2,MultiLineString):
                lines_hit = MultiLineString(lines2)
            else:
                lines_hit = [lines2]

        if tolerance > 0:
            l1 = extend_line(l1, tolerance)

        x = l1.intersection(lines_hit)
        try: x.is_empty 
        except Exception as e: x=x[0]
            
        if not x.is_empty:
            if isinstance(x, Point):
                pnts = [x]
            else:
                if isinstance(x, MultiPoint):
                    pnts = [Point(geom) for geom in x.__geo_interface__["coordinates"]]
                elif isinstance(x, (MultiLineString, MultiPolygon, GeometryCollection)):
                    try:
                        pnts = [Point(coords) for geom in x for coords in geom.coords]
                    except Exception as e:
                        print(i1,e)
                        print(x)
                elif isinstance(x, (LineString, Polygon)):
                    pnts = [Point(coords) for coords in x.coords]
                else:
                    raise NotImplementedError('intersection yields bad type')

            for pnt in pnts:
                if min_spacing > 0:
                    if ipnt > 0:
                        hits = list(tree_idx_pnt.intersection(pnt.bounds))
                    else:
                        hits = []

                    if len(hits) == 0:  # no pnts within spacing
                        ipnt += 1
                        tree_idx_pnt.insert(ipnt, pnt.buffer(min_spacing).bounds)
                        #points.append(pnt)
                        ids.append(i1)
                else:
                    #points.append(pnt)
                    ids.append(i1)
        

    return ids

def fechaHora():
  import datetime as dt
  t = dt.datetime.today()
  return str(t)[:-7].replace(" ","-").replace(":","")

def imp(text):
  import datetime as dt
  t = dt.datetime.today()
  print("|%s|  %s" % (str(t)[5:-5],str(text)))

def dist2pnts(x1, y1, x2, y2):
	return ((x2-x1)**2+(y2-y1)**2)**0.5












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