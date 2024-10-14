from shapely import Point
import folium
import geopandas as gpd
import os

def punto(x,y):
  return Point(x,y)

def plot(gdf):
  m = gdf.explore(column="id", cmap="Set1", name="id", legend=True, popup=True)
  folium.TileLayer('OpenStreetMap').add_to(m)
  folium.LayerControl().add_to(m)
  m.show_in_browser()
  

def sepa(c="*-*-"):
  print("%s" * 20  % tuple([c for i in range(20)]))

def fechaHora():
  import datetime as dt
  t = dt.datetime.today()
  return str(t)[:-7].replace(" ","-").replace(":","")

def imp(text):
  t = dt.datetime.today()
  print("|%s|  %s" % (str(t)[5:-5],str(text)))

def colores(v):
  return "red" if v==True else "gray"
