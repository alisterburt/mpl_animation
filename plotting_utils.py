import numpy as np


def redraw_scatter(drawn_object, new_x, new_y):
    positions = np.vstack((new_x, new_y)).transpose()
    drawn_object.set_offsets(positions)
    return None


def redraw_line(drawn_line, new_x, new_y):
    drawn_line.set_xdata(new_x)
    drawn_line.set_ydata(new_y)
    return None
