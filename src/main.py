import matplotlib.pyplot as plt
from shapely import geometry
from shapely import wkt
import csv
import numpy as np
from time import time
from skimage import measure
import os.path


def point_file_reader(filename):
    points = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            points.append(row)
    return points[1:]


def plot_polygon(poly_lst, filename):
    if type(poly_lst) != list:
        poly_lst = [poly_lst]
    with open(filename, 'w') as csvfile:
        csvfile.write(",polygon\n")
        for ii, poly in enumerate(poly_lst):
            csvfile.write(f'{ii}, "{poly.wkt}"\n')


def gauss_2d(points, sigma, n_grid=100):
    # points = points_df.values
    x_max, y_max = points.max(0)
    x_min, y_min = points.min(0)
    a = 0.13 * max(sigma)
    extra_x = a * 0.5*(x_min + x_max)
    extra_y = a * 0.5*(y_min + y_max)

    x = np.linspace(x_min - extra_x, x_max + extra_x, n_grid)
    y = np.linspace(y_min - extra_y, y_max + extra_y, n_grid)
    xx, yy = np.meshgrid(x, y)
    ga = np.zeros_like(xx)

    for point in points:
        ga += \
            np.exp(-((xx-point[0])**2 / (2.0*sigma[0]**2) + (yy-point[1])**2 / (2.0*sigma[1]**2)))
    ga = ga - ga.min()
    ga = ga/ga.max()
    return xx, yy, ga


def find_contours(x, y, ga, thresh):
    n_x, n_y = len(x), len(y)
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    contour_points_lst = measure.find_contours(ga, thresh)
    for contour in contour_points_lst:
        contour[:, 0] = x_min + ((x_max - x_min) / (n_x - 1)) * contour[:, 0]
        contour[:, 1] = y_min + ((y_max - y_min) / (n_y - 1)) * contour[:, 1]
    return contour_points_lst


def main():
    input_filename = 'double_banana.csv'
    path = os.path.join("input", input_filename)
    points = point_file_reader(path)

    points_list = []
    for point in points:
        points_list.append(wkt.loads(point[1][1:-1]))
    polygon = geometry.Polygon([[p.x, p.y] for p in points_list]).convex_hull
    plot_polygon(polygon, os.path.join('output', 'poly.csv'))
    points = np.array([[point.x, point.y] for point in points_list])
    t0 = time()
    # sigma = 0.0025
    # Experimental sigma:
    sigma = 0.013 * (len(points_list) / (polygon.area*1000)) ** (-0.273)
    sigma_xy = [sigma, sigma]
    xx, yy, ga = gauss_2d(points, sigma_xy, n_grid=100)
    t1 = time()
    contour_point_lst = find_contours(xx[0, :], yy[:, 0], ga.T, 0.1)
    contours_shp = []
    intersect_shp = []
    for contour in contour_point_lst:
        contours_shp.append(geometry.Polygon(contour))
        intersect_shp.append(polygon.intersection(contours_shp[-1]))
    t2 = time()
    plot_polygon(contours_shp, os.path.join('output', 'contour.csv'))
    t3 = time()
    plot_polygon(intersect_shp, os.path.join('output', 'intersect.csv'))
    plt.contour(xx, yy, ga, 15)
    for contour in contour_point_lst:
        plt.plot(contour[:, 0], contour[:, 1], 'r--')
    plt.axis('square')
    plt.grid()
    # plt.show()
    print(f"gaussian time:  {t1 - t0:0.5f}\n"
          f"contour time:   {t2 - t1:0.5f}\n"
          f"intersect time: {t3 - t3:0.5f}")

    print('end of file')


if __name__ == '__main__':
    main()
