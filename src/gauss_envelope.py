from shapely import geometry
from shapely import wkt
import numpy as np
from skimage import measure


class GaussEnvelope:
    def __init__(self, points):
        self.polygon = None
        self.contour_point_lst = None
        self.xx = None
        self.yy = None
        self.gauss_grid = None
        self.points = points
        self.sigma = None
        self.grid_size = None
        # self.mk_convex_polygon()
        # self.mk_grid()
        # self.find_contours()

    def mk_grid(self, grid_size):
        x_max, y_max = self.points.max(0)
        x_min, y_min = self.points.min(0)
        a = 0.13 * self.sigma
        extra_x = a * np.mean([x_min, x_max])
        extra_y = a * np.mean([y_min, y_max])
        x = np.linspace(x_min - extra_x, x_max + extra_x, grid_size)
        y = np.linspace(y_min - extra_y, y_max + extra_y, grid_size)
        self.xx, self.yy = np.meshgrid(x, y)

    def calc_gauss_grid(self, sigma, grid_size=100):
        self.sigma = sigma
        self.mk_grid(grid_size=grid_size)
        self.gauss_grid = np.zeros_like(self.xx)
        for point in self.points:
            self.gauss_grid += \
                np.exp(-((self.xx - point[0]) ** 2 + (self.yy - point[1]) ** 2) / (2.0 * self.sigma ** 2))
        # Normalize:
        self.gauss_grid = self.gauss_grid - self.gauss_grid.min()
        self.gauss_grid = self.gauss_grid / self.gauss_grid.max()

    def find_contours(self, thresh):
        n_x, n_y = len(self.xx[0, :]), len(self.yy[:, 0])
        x_min, x_max = self.xx[0, :].min(), self.xx[0, :].max()
        y_min, y_max = self.yy[:, 0].min(), self.yy[:, 0].max()
        self.contour_point_lst = measure.find_contours(self.gauss_grid.T, thresh)
        for contour in self.contour_point_lst:
            contour[:, 0] = x_min + ((x_max - x_min) / (n_x - 1)) * contour[:, 0]
            contour[:, 1] = y_min + ((y_max - y_min) / (n_y - 1)) * contour[:, 1]

    def mk_convex_polygon(self, return_value=False):
        self.polygon = geometry.Polygon(self.points).convex_hull
        if return_value:
            return self.polygon


