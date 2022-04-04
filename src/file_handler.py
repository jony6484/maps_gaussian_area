from shapely import geometry
from shapely import wkt
import csv
import numpy as np


def point_file_reader(lines):
    lines = lines[1:-1]
    points_list = []
    # skip th header
    for line in lines:
        points_list.append(wkt.loads(line.split(',')[1][1:-1]))
    points_arr = np.array([[point.x, point.y] for point in points_list])
    return points_list, points_arr
