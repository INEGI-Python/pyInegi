import numpy as np


def remove_colinear_points(geom, angulo):
		if geom.geom_type == "Polygon":
			coords = list(geom.exterior.coords)
			if len(coords)>5:
				new_coords = [coords[0]]
				for i in range(1, len(coords) -1):
					p0 = np.array(new_coords[-1])
					p1 = np.array(coords[i])
					p2 = np.array(coords[i + 1])
					v1 = p1 - p0
					v2 = p2 - p1
					cross = np.cross(v1, v2)
					angle = np.arctan2(np.linalg.norm(cross), np.dot(v1, v2))
					angle_deg = np.degrees(angle)
					if np.abs(angle_deg) >= angulo:
						new_coords.append(coords[i])
				new_coords.append(coords[-1])
				return type(geom)(new_coords)
		return geom