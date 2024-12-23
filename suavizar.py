import matplotlib.pyplot as plt
import geopandas as gpd
from shapely import geometry
import topojson

x_min, x_max, y_min, y_max = 0, 20, 0, 20

## Create original (coarse) polygons:
staircase_points = [[(ii, ii), (ii, ii + 1)] for ii in range(x_max)]
staircase_points_flat = [
    coord for double_coord in staircase_points for coord in double_coord
] + [(x_max, y_max)]

list_points = {
    1: staircase_points_flat + [(x_max, y_min)],
    2: staircase_points_flat[1:-1] + [(x_min, y_max)],
}
pols_coarse = {}
for ind_pol in [1, 2]:
    list_points[ind_pol] = [geometry.Point(x) for x in list_points[ind_pol]]
    pols_coarse[ind_pol] = geometry.Polygon(list_points[ind_pol])

df_pols_coarse = gpd.GeoDataFrame(
    {"geometry": pols_coarse.values(), "id": pols_coarse.keys()}
)

## Create smooth polygons:
topo = topojson.Topology(df_pols_coarse)
topo_smooth = topo.toposimplify(1)
df_pols_smooth = topo_smooth.to_gdf()

## Plot
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
df_pols_coarse.plot(column="id", ax=ax[0])
df_pols_smooth.plot(column="id", ax=ax[1])
ax[0].set_title("Original polygons")
ax[1].set_title("Smoothed polygons")
plt.show()