import numpy as np


def get_nan_fitmap(fit_map, mask, i):
    mask[mask != i] = 0
    mask[mask == i] = 1
    fit_map = np.multiply(fit_map, mask)
    fit_map = np.where(fit_map != 0.0, fit_map, np.nan)
    return mask, fit_map