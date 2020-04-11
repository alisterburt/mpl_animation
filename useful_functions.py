import numpy as np


def smootherstep(n):
    points = np.linspace(0, 1, n)
    points[1:-1] = (6 * points[1:-1] ** 5) - (15 * points[1:-1] ** 4) + (10 * points[1:-1] ** 3)
    return points


def smooth_rotation_increments(n, max_rotation=2*np.pi):
    cumulative_angles = max_rotation * smootherstep(n + 1)
    angles = cumulative_angles[1:] - cumulative_angles[:-1]
    return angles

