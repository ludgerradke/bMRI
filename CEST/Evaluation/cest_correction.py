import numpy as np
from CEST.Utils import matlab_style_functions
from multiprocessing import Pool


def cest_correction(cest_array, x_calcentires, x, x_itp, mask, offset_map, interpolation, cest_range,
                    multiprocessing=True):
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

    arguments = np.argwhere(mask != 0)
    if multiprocessing:
        with Pool() as pool:
            idxs, correction = zip(
                *pool.map(cest_correction_process, [(cest_range, cest_array[:, i, j, k], offset_map[i, j, k],
                                                     x_itp, x, interpolation, [k, i, j]) for i, j, k in arguments]))
            for n in range(len(idxs)):
                k, i, j = idxs[n]
                CestCurveS[i, j, k, :] = correction[n]
    else:
        for i, j, k in arguments:
            values = cest_array[:, i, j, k]
            offset = offset_map[i, j, k]
            CestCurveS[i, j, k, :] = calc_pixel(cest_range, values, offset, x_itp, x, interpolation)

    return CestCurveS, x_calcentires


def cest_correction_process(arguments):
    arguments = list(arguments)
    return arguments[-1], calc_pixel(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])


def calc_pixel(range, y_values, offset, x_itp, x, interpolation):
    y_itp = matlab_style_functions.interpolate(x, y_values, x_itp, interpolation)

    vind_sC_1 = abs(x_itp - (-range + offset))
    vind_sC_2 = abs(x_itp - (range + offset))
    ind_sC_1 = np.argmin(vind_sC_1)
    ind_sC_2 = np.argmin(vind_sC_2)

    y_calcentries = y_itp[ind_sC_1: ind_sC_2 + 1]
    return y_calcentries
