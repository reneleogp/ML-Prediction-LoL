import numpy as np
import scipy.stats


def median(array):
    return np.median(array)


def average(array):
    return np.average(array)


def kurtosis(array):
    return scipy.stats.kurtosis(array, bias=False)


def skewness(array):
    return scipy.stats.skew(array, bias=False)


def standard_deviation(array):
    return np.std(array)


def variance(array):
    return np.var(array)
