import numpy as np
import math


def calc_mtr_asym(CestCurveS, x_calcentires, mask, d_shift, f_shift, hStep):
    (rows, colums, z_slices, entires) = CestCurveS.shape
    entry_mtr = math.ceil(entires / 2)

    mtr_asym_curves = np.zeros((rows, colums, z_slices, entry_mtr), dtype=float)
    mtr_asym_img = np.zeros((rows, colums, z_slices), dtype=float)
    for k in range(z_slices):
        for i in range(rows):
            for j in range(colums):
                if mask[i, j, k] != 0:
                    mtr_asym_curves[i, j, k, :], mtr_asym_img[i, j, k] = \
                        calc_mtr_asym_pixel(entry_mtr, CestCurveS[i, j, k, :], d_shift, f_shift,
                                            x_calcentires, hStep)
    return mtr_asym_curves, mtr_asym_img


def calc_mtr_asym_pixel(entry_mtr, values, d_shift, f_shift, x_calcentires, hStep):
    mtra = np.flip(values[:entry_mtr]) - values[entry_mtr - 1:]
    mtra = mtra * 100

    range = (f_shift - d_shift / 2, f_shift + d_shift / 2)
    x_mrt_calcentries = x_calcentires[entry_mtr - 1:]
    vind1 = np.argmin(abs(x_mrt_calcentries - range[0]))
    vind2 = np.argmin(abs(x_mrt_calcentries - range[1]))

    asym = mtra[vind1: vind2 + 1]
    asym_value = np.sum(asym) * hStep
    return mtra, asym_value