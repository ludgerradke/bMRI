from Utilitis import get_dcm_list, split_dcm_List, get_dcm_array
import numpy as np
from Fitting.AbstractFitting import AbstractFitting
import pydicom
from glob import glob


def fit_(x, S0, t2_t2star, offset):
    return S0 * np.exp(-x / t2_t2star) + offset


def get_prep_fit(TR, T1, alpha, TE, T2star):
    def fit_(x, S0, t2_t2star, offset):
        counter = np.sin(alpha)*(1-np.exp(-TR/T1))*np.exp(-TE/T2star)
        denominator = (1-np.cos(alpha)*np.exp(-TR/T1))
        return S0*counter/denominator * np.exp(-x/t2_t2star) + offset
    return fit_


class T2_T2star(AbstractFitting):
    """
    Class for the calculation of T1 times

    Args:
        dim (int): Dimension of the images (2 or 3D)
        folder (str): path to the dicom images
        bounds (tuple([len(n)], [len(n)]): Bounds values of the fit function bounds = ([x_min, y_min, z_min],
            [x_max, y_max, z_max]).
            Note: The bounds are handed in according to the scipy.optimize.curve_fit convention.
        config (dict): Dict in which the essential information is required for the fitting function
            with preparation pules.
        """
    def __init__(self, dim, folder, bounds, config=None):
        if config is not None:
            if all(i in ["T1", "TR", "alpha", "TE", "T2star"] for i in config.keys()):
                fit = get_prep_fit(config["TR"], config["T1"], config["alpha"], config["TE"], config["T2star"])
            else:
                raise UserWarning
        else:
            fit = fit_
        super(T2_T2star, self).__init__(dim, folder, fit, bounds)
        self.load()

    def load(self):
        """
        load dicom images and Echo times
        """
        if self.dim == 2:
            dcm_files = get_dcm_list(self.folder + '\\')
            self.get_tes(dcm_files)
            dcm_files = [[dcm] for dcm in dcm_files]
        if self.dim == 3:
            dcm_files = get_dcm_list(self.folder + '\\')
            if len(dcm_files) == 0:
                echos = glob(self.folder + r'\\*\\')
                dcm_files = [get_dcm_list(echo) for echo in echos]
                dcm_files = [item for sublist in dcm_files for item in sublist]
            self.get_tes(dcm_files)
            dcm_files = split_dcm_List(dcm_files, True)
        # self.array == echos, z, x, y --> echos, x, y, z
        self.array = np.array([get_dcm_array(dcm) for dcm in dcm_files]).transpose(0, 3, 2, 1)

    def get_tes(self, dcm_files):
        x = []
        for dcm in dcm_files:
            info = pydicom.dcmread(dcm)
            if info.EchoTime not in x:
                x.append(info.EchoTime)
        self.x = [float(te) for te in x]
