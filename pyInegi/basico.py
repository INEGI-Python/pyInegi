from shapely import Point
import folium
import geopandas as gpd
import os
print(os.getcwd())

def punto(x,y):
  return Point(x,y)

def plot(gdf):
  m = gdf.explore(column="id", cmap="Set1", name="id", legend=True, popup=True)
  folium.TileLayer('OpenStreetMap').add_to(m)
  folium.LayerControl().add_to(m)
  m.show_in_browser()
  

