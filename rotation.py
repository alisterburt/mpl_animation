import numpy as np


def rotate_2d(x, y, theta=None, theta_degrees=None, origin=(0, 0)):
    x_to_rotate = np.asarray(x) - origin[0]
    y_to_rotate = np.asarray(y) - origin[1]

    if theta_degrees is not None:
        theta = (theta_degrees / 360) * (2 * np.pi)

    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    rotm = [[cos_theta, -sin_theta],
            [sin_theta, cos_theta]]

    xy = np.vstack((x_to_rotate, y_to_rotate))

    xy_rotated = rotm @ xy

    x = xy_rotated[0] + origin[0]
    y = xy_rotated[1] + origin[1]

    return x, y

