import numpy as np
from periodic_functions import sin, cos
from rotation import rotate_2d


def circle(n_points, radius=1, phase_shift=0, origin=(0, 0)):
    x = cos(n_points, amplitude=radius, phase_shift=phase_shift)
    y = sin(n_points, amplitude=radius, phase_shift=phase_shift)

    x = x + origin[0]
    y = y + origin[0]

    return x, y


def regular_polygon(n_sides, size=1, phase_shift=0):
    x, y = circle(n_points=n_sides, phase_shift=phase_shift + (np.pi / 2))
    for dim in x, y:
        dim = dim * size
    return x, y


def linspace_shift(start, stop, n_points, phase_shift):
    v = np.linspace(0, 2 * np.pi, n_points + 1)[:-1]
    v += phase_shift
    v = np.mod(v, 2 * np.pi)

    range = np.ptp((start, stop))
    v = (v / (2 * np.pi)) * range
    v += start
    return v


def length(x, y):
    l = np.sqrt(x**2 + y**2)
    return l


# def points_along_polygon(x, y, n_points, phase_shift=0):
#     n_points = np.asarray(x).shape[0]
#     total_length = 0
#     for idx in range(n_points):
#         if idx == n_points - 1:
#             current_segment_start = np.asarray((x[idx], y[idx]))
#             current_segment_end = np.asarray(x[0], y[0])
#         else:
#             current_segment_start = np.asarray((x[idx], y[idx]))
#             current_segment_end = np.asarray(x[idx + 1], y[idx + 1])

#
# def points_along_regular_polygon(n_points, n_sides, phase_shift_points=0, phase_shift_polygon=0):
#     theta_points = linspace_shift(0, 2*np.pi, n_points=n_points, phase_shift=phase_shift_points)
#     theta_corners = linspace_shift(0, 2 * np.pi, n_points=n_sides, phase_shift=phase_shift_polygon)
#
#     corners_x, corners_y = regular_polygon(n_sides, phase_shift_polygon)
#
#     edges = np.zeros((n_sides, 2, 2))
#     for edge_idx in range(n_sides):



def edges_from_corners(x, y):
    """
    computes edges from x, y vectors describing corners of a polygon
    :param x: x position of corner
    :param y: y position of corner
    :return: x_edges, y_edges, (n_edges, 2, 2), dim 1 = edge, dim2 = start,end, dim3 = x, y
    """
    x = np.asarray(x)
    y = np.asarray(y)

    n_edges = np.asarray(x).shape[0]
    edges = np.zeros((n_edges, 2, 2))

    for edge_idx in range(n_edges):
        if edge_idx == n_edges - 1:
            edges[edge_idx, 0, :] = [x[edge_idx], y[edge_idx]]
            edges[edge_idx, 1, :] = [x[0], y[0]]
        else:
            edges[edge_idx, 0, :] = [x[edge_idx], y[edge_idx]]
            edges[edge_idx, 1, :] = [x[edge_idx + 1], y[edge_idx + 1]]

    return edges


# import matplotlib.pyplot as plt
#
# x, y = regular_polygon(13, 3.14 / 2 )
# x2, y2, e = edges_from_corners(x, y)
# fig, ax = plt.subplots()
#
# ax.plot(x2-2,y2-2)
# for idx, edge in enumerate(e):
#     x = edge[:, 0]
#     y = edge[:, 1]
#     ax.plot(x,y, label=f'edge {idx}')
# ax.set_aspect('equal')
# ax.legend()


class RegularPolygon:
    def __init__(self, n_edges, size=1, origin=(0,0)):
        corners_x, corners_y = regular_polygon(n_edges, size=size, phase_shift=0)
        self.corners = corners_x + origin[0], corners_y + origin[1]
        self.origin = origin
        self.edges = edges_from_corners(self.corners[0], self.corners[1])
        self.n_edges = self.edges.shape[0]

    def get_edges_from_corners(self):
        x_edges = np.zeros(self.n_edges + 1)
        y_edges = np.zeros(self.n_edges + 1)

        x_edges[:-1] = self.corners[0]
        x_edges[-1] = x_edges[0]

        y_edges[:-1] = self.corners[1]
        y_edges[-1] = y_edges[0]
        return x_edges, y_edges

    def get_all_edges(self):
        edges = [self.get_edge(edge_idx) for edge_idx in range(self.n_edges)]
        return edges

    def get_edge(self, edge_index):
        edge = self.edges[edge_index]
        x = edge[:, 0]
        y = edge[:, 1]
        return x, y

    def set_edge(self, edge_index, x, y):
        self.edges[edge_index][:, 0] = x
        self.edges[edge_index][:, 1] = y
        return None

    def get_edge_center(self, edge_index):
        edge_x, edge_y = self.get_edge(edge_index)
        x = np.mean(edge_x)
        y = np.mean(edge_y)
        return x, y

    def get_all_corners(self):
        x = self.corners[0]
        y = self.corners[1]
        return x, y

    def get_corner(self, corner_index):
        x = self.corners[0][corner_index]
        y = self.corners[1][corner_index]
        return x, y

    def rotate(self, theta, origin=None):
        if origin is not None:
            self.rotate_all_edge_extremities(theta)
            self.rotate_all_edge_centers(theta, origin=origin)
            self.rotate_all_corners(theta, origin=origin)
        else:
            self.rotate(theta, origin=self.origin)
        return None

    def rotate_all_corners(self, theta, origin=None):
        corners_x = self.corners[0]
        corners_y = self.corners[1]

        if origin is not None:
            self.corners = rotate_2d(corners_x, corners_y, theta=theta, origin=origin)
        else:
            self.corners = rotate_2d(corners_x, corners_y, theta=theta, origin=self.origin)

        return None

    def rotate_corner(self, corner_index, theta, origin=None):
        corner_x, corner_y = self.get_corner(corner_index)

        if origin is not None:
            corner_x_rotated = rotate_2d(corner_x, corner_y, theta=theta, origin=origin)
        else:
            corner_y_rotated = rotate_2d(corner_x, corner_y, theta=theta, origin=self.origin)

        return None

    def rotate_all_edge_centers(self, theta, origin=None):
        for edge_idx in range(self.n_edges):
            if origin is not None:
                self.rotate_edge_center(edge_idx, theta=theta, origin=origin)
            else:
                self.rotate_edge_center(edge_idx, theta=theta, origin=self.origin)

        return None

    def rotate_all_edge_extremities(self, theta, origin=None):
        for edge_idx in range(self.n_edges):
            self.rotate_edge_extremities(edge_idx, theta, origin=origin)

        return None

    def rotate_edge_extremities(self, edge_index, theta, origin=None):
        edge_x, edge_y = self.get_edge(edge_index)
        if origin is None:
            origin = self.get_edge_center(edge_index)

        edge_x_rotated, edge_y_rotated = rotate_2d(edge_x, edge_y, theta, origin=origin)
        self.set_edge(edge_index, edge_x_rotated, edge_y_rotated)
        return None

    def rotate_edge_center(self, edge_index, theta, origin=None):
        edge_x, edge_y = self.get_edge(edge_index)
        edge_center_x, edge_center_y = self.get_edge_center(edge_index)
        edge_dx = edge_x - edge_center_x
        edge_dy = edge_y - edge_center_y
        if origin is None:
            origin = self.get_edge_center(edge_index)

        edge_center_rotated_x, edge_center_rotated_y = rotate_2d(edge_center_x,
                                                                 edge_center_y,
                                                                 theta=theta,
                                                                 origin=origin)

        x = edge_center_rotated_x + edge_dx
        y = edge_center_rotated_y + edge_dy

        self.set_edge(edge_index, x, y)
        return None

    def rotate_edge_around_start(self, edge_index, theta):
        edge_x, edge_y = self.get_edge(edge_index)
        rotation_center = (edge_x[0], edge_y[0])

        edge_x_rotated, edge_y_rotated = rotate_2d(edge_x, edge_y, theta=theta, origin=rotation_center)
        self.set_edge(edge_index, edge_x_rotated, edge_y_rotated)
        return None

    def rotate_edge_around_end(self, edge_index, theta):
        edge_x, edge_y = self.get_edge(edge_index)
        rotation_center = (edge_x[-1], edge_y[-1])

        edge_x_rotated, edge_y_rotated = rotate_2d(edge_x, edge_y, theta=theta, origin=rotation_center)
        self.set_edge(edge_index, edge_x_rotated, edge_y_rotated)
        return None

    def rotate_all_edges_around_start(self, theta):
        for edge_idx in range(self.n_edges):
            self.rotate_edge_around_start(edge_idx, theta=theta)
        return None

    def rotate_all_edges_around_end(self, theta):
        for edge_idx in range(self.n_edges):
            self.rotate_edge_around_end(edge_idx, theta=theta)
        return None



#
# class Square(regular_polygon):
#     def __init__(self, size, phase_shift=0):


# import matplotlib.pyplot as plt
#
#
# def plot_square(ax):
#     x, y = square.get_all_corners()
#     ax.scatter(x,y)
#     for idx, edge in enumerate(square.edges):
#         edge_x = edge[:, 0]
#         edge_y = edge[:, 1]
#         ax.plot(edge_x, edge_y, label=f'edge {idx}')
#     ax.set_aspect('equal')
#     ax.set_xlim(-1.5, 1.5)
#     ax.set_ylim(-1.5, 1.5)
#     return None
#
# square = RegularPolygon(4)
# fig, axes = plt.subplots(5)
# plot_square(axes[0])
# square.rotate_all_edge_extremities(np.deg2rad(45))
# plot_square(axes[1])
# square.rotate_all_edge_centers(np.deg2rad(45))
# plot_square(axes[2])
# square.rotate_all_corners(np.deg2rad(45))
# plot_square(axes[3])
#
# square = RegularPolygon(4)
# square.rotate_object(np.deg2rad(45))
# plot_square(axes[4])
#
