import numpy as np


def remove_colinear_points(geom, tolerance=5):
		if geom.geom_type == "Polygon":
			coords = list(geom.exterior.coords)
			new_coords = [coords[0]]
			for i in range(1, len(coords) - 1):
				p0 = np.array(new_coords[-1])
				p1 = np.array(coords[i])
				p2 = np.array(coords[i + 1])
				v1 = p1 - p0
				v2 = p2 - p1
				cross = np.cross(v1, v2)
				if np.abs(cross) > tolerance:
					new_coords.append(coords[i])
			new_coords.append(coords[-1])
			return type(geom)(new_coords)
		return geom