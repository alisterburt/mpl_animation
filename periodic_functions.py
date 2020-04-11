import numpy as np


def sin(n_points, amplitude=1, periods=1, phase_shift=0):
    """

    :param n_points: number of points to produce along the function
    :param amplitude: amplitude of wave
    :param frequency: number of periods to produce
    :param phase_shift: phase shift of signal in radians
    :return:
    """
    theta = np.linspace(0, 2*np.pi, n_points + 1)[:-1]
    return amplitude * np.sin((periods * theta) + phase_shift)


def cos(n_points, amplitude=1, periods=1, phase_shift=0):
    """

    :param n_points: number of points to produce along the function
    :param amplitude: amplitude of wave
    :param frequency: number of periods to produce
    :param phase_shift: phase shift of signal in radians
    :return: periodic cosine function for
    """
    theta = np.linspace(0, 2*np.pi, n_points + 1)[:-1]
    return amplitude * np.cos((periods * theta) + phase_shift)


