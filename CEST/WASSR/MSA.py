######################################################################################
# msa = Maximum Symmetry Algorithm                                                   #
# Reference:    WAter Saturation Shift Referencing (WASSR) for chemical              #
#               exchange saturation transfer experiments                             #
#               DOI:     10.1002/mrm.21873                                           #
#               Authors: Kim et al. 2009                                             #
######################################################################################

import numpy as np
from CEST.Utils import matlab_style_functions
from CEST.WASSR.algorithm import Algorithm


class MSA(Algorithm):

    def __init__(self, config):
        super(MSA, self).__init__()
        self.hStep = float(config.itp_step)
        self.maxOffset = float(config.wassr_offset)
        self.maxShift = float(config.max_wassr_shift)

    def calculate(self, ppms, values):
        if abs(ppms[np.argmin(values)]) > self.maxShift:
            return -100
        dppm = self.maxShift
        x_start = np.min(ppms)
        x_end = np.max(ppms)

        x_interp = np.arange(x_start, x_end, self.hStep).transpose()
        x_interp = np.append(x_interp, x_end)
        x_interp_mirror = -x_interp

        y_interp = matlab_style_functions.interpolate(ppms, values, x_interp, "quadratic")
        minind = np.argmin(y_interp)

        xsuch = round(x_interp[minind] * 100) / 100
        xsuch_minus = xsuch - dppm
        xsuch_plus = xsuch + dppm

        if xsuch_minus <= x_start:
            xsuch_minus = x_start

        if xsuch_plus >= x_end:
            xsuch_plus = x_end

        x_interp_neu = np.arange(xsuch_minus, xsuch_plus, self.hStep).transpose()
        x_interp_neu = np.append(x_interp_neu, xsuch_plus)

        y_interp_neu = matlab_style_functions.interpolatePChip1D(ppms, values, x_interp_neu)

        OF = self.msa(x_interp_neu, y_interp_neu, x_interp_mirror, y_interp)

        if OF > self.maxShift:
            return -100
        return OF

    def msa(self, xWerte, yWerte, x_interp_mirror, y_interp):
        n_points = len(xWerte)
        minind = np.argmin(yWerte)
        x_search = round(xWerte[minind] * 100) / 100

        start_Abt = x_search - self.maxShift
        if start_Abt <= -self.maxOffset:
            start_Abt = -self.maxOffset

        ende_Abt = x_search + self.maxShift
        if ende_Abt >= self.maxOffset:
            ende_Abt = self.maxOffset

        AbtastvektorC = np.arange(start_Abt, ende_Abt, self.hStep).transpose()
        AbtastvektorC = np.append(AbtastvektorC, ende_Abt)
        siyAC = len(AbtastvektorC)

        MSCF = np.zeros((siyAC), dtype=float)

        for i in range(0, siyAC):
            C = AbtastvektorC[i]
            Xwert_verschobenmirror = np.zeros((n_points), dtype=float)
            Ywert_verschobenmirror = np.zeros((n_points), dtype=float)

            for j in range(0, n_points):
                xn = xWerte[j]
                x_interp_mirror_versch = x_interp_mirror + 2 * C
                V_x_interp_mirror_versch = abs(x_interp_mirror_versch - xn)
                index = np.argmin(V_x_interp_mirror_versch)
                Xwert_verschobenmirror[j] = x_interp_mirror_versch[index]
                Ywert_verschobenmirror[j] = y_interp[index]

            MSE_Vektor = (Ywert_verschobenmirror - yWerte) * (Ywert_verschobenmirror - yWerte)
            MSCF[i] = MSE_Vektor.sum()

        indexmin = np.argmin(MSCF)
        return AbtastvektorC[indexmin]


