from Utilitis import get_dcm_list, split_dcm_List, get_dcm_array
from glob import glob
import numpy as np
from Fitting.AbstractFitting import AbstractFitting


def fit_(x, S0, t1rho, offset):
    return S0 * np.exp(-x / t1rho) + offset


def get_short_TR_fit(TR, T1, alpha):
        def short_TR_fit(x, S0, t1rho, offset):

            counter = (np.exp(-x / t1rho)) * (1 - np.exp(-(TR - x) / T1)) * np.sin(alpha)
            denominator = 1-np.exp(-x/t1rho)*np.exp(-(TR - x)/T1)*np.cos(alpha)

            return S0 * counter / denominator + offset
        return short_TR_fit


class T1rho(AbstractFitting):
    """
    Class for the calculation of T1rho times

    Args:
        dim (int): Dimension of the images (2 or 3D)
        folder (str): path to the dicom images
        bounds (tuple([len(n)], [len(n)]): Bounds values of the fit function bounds = ([x_min, y_min, z_min],
            [x_max, y_max, z_max]).
            Note: The bounds are handed in according to the scipy.optimize.curve_fit convention.
        config (dict): Dict in which the essential information is required for the fitting function
            with short TR times.
    """
    def __init__(self, dim, folder, bounds=None, config: dict = None):

        if config is not None:
            if all(i in ["T1", "TR", "alpha"] for i in config.keys()):
                fit = get_short_TR_fit(config["TR"], config["T1"], config["alpha"])
            else:
                raise UserWarning
        else:
            fit = fit_
        super(T1rho, self).__init__(dim, folder, fit, bounds)
        self.load()

    def load(self):
        """
        load dicom images
        """
        if self.dim == 2:
            dcm_files = get_dcm_list(self.folder + '\\')
            dcm_files = [[dcm] for dcm in dcm_files]
        if self.dim == 3:
            echos = glob(self.folder + r'\\*\\')
            if len(echos) != 0:
                dcm_files = [get_dcm_list(echo) for echo in echos]
                dcm_files_flatted = [item for sublist in dcm_files for item in sublist]
            else:
                dcm_files_flatted = glob(self.folder + r'\\*')
            dcm_files = split_dcm_List(dcm_files_flatted, sort=True)
        # self.array == echos, z, x, y --> echos, x, y, z
        self.array = np.array([get_dcm_array(dcm) for dcm in dcm_files]).transpose(0, 3, 2, 1)
