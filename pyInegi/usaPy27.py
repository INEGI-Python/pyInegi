from arcpy.management import SelectLayerByLocation as sL, DeleteFeatures as dF, Delete as d
sL("../esqueletor.shp","INTERSECT","../poligono.shp")
dF("../esqueletor.shp")
d("../poligono.shp")