import numpy as np
from CEST.Utils import matlab_style_functions


def cest_correction(cest_array, x_calcentires, x, x_itp, mask, offset_map, interpolation, cest_range):
    """

    Args:
        cest_array (np.array):
        x_calcentires (np.array):
        x (np.array):
        x_itp (np.array):
        mask (np.array):
        offset_map (np.array):
        interpolation (str):
    """
    (dyn, rows, colums, z_slices) = cest_array.shape
    CestCurveS = np.zeros((rows, colums, z_slices, len(x_calcentires)))

    for k in range(z_slices):
        for i in range(rows):
            for j in range(colums):
                if mask[i, j, k] != 0:
                    values = cest_array[:, i, j, k]
                    offset = offset_map[i, j, k]
                    CestCurveS[i, j, k, :] = calc_pixel(cest_range, values, offset, x_itp, x, interpolation)
    CestCurveS = CestCurveS
    x_calcentires = x_calcentires
    return CestCurveS, x_calcentires


def calc_pixel(range, y_values, offset, x_itp, x, interpolation):
    y_itp = matlab_style_functions.interpolate(x, y_values, x_itp, interpolation)

    vind_sC_1 = abs(x_itp - (-range + offset))
    vind_sC_2 = abs(x_itp - (range + offset))
    ind_sC_1 = np.argmin(vind_sC_1)
    ind_sC_2 = np.argmin(vind_sC_2)

    y_calcentries = y_itp[ind_sC_1: ind_sC_2 + 1]
    return y_calcentries