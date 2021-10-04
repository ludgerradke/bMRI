import numpy as np
import math
from scipy.optimize import curve_fit


def calc_lorentzian(CestCurveS, x_calcentires, mask, config):
    (rows, colums, z_slices, entires) = CestCurveS.shape

    lorenzian = {key: np.zeros((rows, colums, z_slices), dtype=float) for key in config.lorenzian_keys}
    for k in range(z_slices):
        for i in range(rows):
            for j in range(colums):
                if mask[i, j, k] != 0:
                    params = calc_lorenzian_pixel(CestCurveS[i, j, k, :], x_calcentires, config.Lorenzian['MT_f'],
                                                  config.Lorenzian['NOE1_f'], config.Lorenzian['NOE2_f'],
                                                  config.Lorenzian['OH_f'], config.Lorenzian['NH_f'])
                    if params is None:
                        continue
                    dic = {
                        'OH_a': params[3],
                        'OH_w': params[4],
                        'NH_a': params[5],
                        'NH_w': params[6],
                        'NOE1_a': params[7],
                        'NOE1_w': params[8],
                        'NOE2_a': params[9],
                        'NOE2_w': params[10],
                        'MT_a': params[11],
                        'MT_w': params[12],
                    }
                    for key in config.lorenzian_keys:
                        lorenzian[key][i, j, k] = dic[key]
    return lorenzian


def calc_lorenzian_pixel(values, x_calcentires, MT_f, NOE1_f, NOE2_f, OH_f, NH_f):
    # wassr_offset, da die Z-Spektren vorher korrigiert wurden
    fit = lorenz_like_matlab(wassr_offset=0, MT_f=MT_f, NOE1_f=NOE1_f, NOE2_f=NOE2_f, OH_f=OH_f, NH_f=NH_f)
    try:
        param, param_cov = curve_fit(fit, x_calcentires, values, bounds=([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                                         [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                                                          10,
                                                                          10]))
    except RuntimeError:
        param = None

    return param


def lorenz_like_matlab(wassr_offset, MT_f: float = - 2.43, NOE1_f: float = - 1, NOE2_f: float = - 2.6,
                       OH_f: float = + 1.4, NH_f: float = + 3.2):
    # X_f = frequenz of X
    #ret = (a + ak) - (a * ((b ** 2) / 4) / (((b ** 2) / 4) + (x - wassr_offset) ** 2))
    pass

def one_lorenz(x, amplitude, width, wassr_offset, frequenz):
    return amplitude * ((width ** 2) / 4) / (((width ** 2) / 4) + (x - (wassr_offset + frequenz)) ** 2)
