import matplotlib.pyplot as plt
from shapely import geometry
from shapely import wkt
import csv
import numpy as np
from time import time
from skimage import measure
import os.path
from src.gauss_envelope import GaussEnvelope
from file_handler import point_file_reader


def plot_polygon(poly_lst, filename):
    if type(poly_lst) != list:
        poly_lst = [poly_lst]
    with open(filename, 'w') as csvfile:
        csvfile.write(",polygon\n")
        for ii, poly in enumerate(poly_lst):
            csvfile.write(f'{ii}, "{poly.wkt}"\n')


def main():
    input_filename = 'double_banana.csv'
    path = os.path.join("input", input_filename)
    with open(path, newline='') as csvfile:
        lines = csvfile.read().split('\n')
        points_list, points_arr = point_file_reader(lines)
    gauss_env = GaussEnvelope(points_arr)
    polygon = gauss_env.mk_convex_polygon(return_value=True)
    plot_polygon(polygon, os.path.join('output', 'poly.csv'))
    # sigma = 0.0025
    # Experimental sigma:
    sigma = 0.013 * (len(points_list) / (polygon.area * 1000)) ** (-0.273)
    gauss_env.calc_gauss_grid(sigma=sigma)
    gauss_env.find_contours(thresh=0.1)
    t0 = time()
    t1 = time()

    contours_shp = []
    intersect_shp = []
    for contour in gauss_env.contour_point_lst:
        contours_shp.append(geometry.Polygon(contour))
        intersect_shp.append(polygon.intersection(contours_shp[-1]))
    t2 = time()
    plot_polygon(contours_shp, os.path.join('output', 'contour.csv'))
    t3 = time()
    plot_polygon(intersect_shp, os.path.join('output', 'intersect.csv'))
    plt.contour(gauss_env.xx, gauss_env.yy, gauss_env.gauss_grid, 15)
    for contour in gauss_env.contour_point_lst:
        plt.plot(contour[:, 0], contour[:, 1], 'r--')
    plt.axis('square')
    plt.grid()
    plt.show()
    print(f"gaussian time:  {t1 - t0:0.5f}\n"
          f"contour time:   {t2 - t1:0.5f}\n"
          f"intersect time: {t3 - t3:0.5f}")

    print('end of file')


if __name__ == '__main__':
    main()
