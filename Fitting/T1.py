from Utilitis import get_dcm_list, split_dcm_List, get_dcm_array
import numpy as np
from Fitting.AbstractFitting import AbstractFitting
import pydicom
from glob import glob


def inversion_recovery_t1(x, S0, t1, offset):
    return S0 * (1 - np.exp(-x / t1)) + offset


class T1(AbstractFitting):
    """
    Class for the calculation of T1 times

    Args:
        dim (int): Dimension of the images (2 or 3D)
        folder (str): path to the dicom images
        bounds (tuple([len(n)], [len(n)]): Bounds values of the fit function bounds = ([x_min, y_min, z_min],
            [x_max, y_max, z_max]).
            Note: The bounds are handed in according to the scipy.optimize.curve_fit convention.
    """
    def __init__(self, dim: int, folder: str, bounds):
        super(T1, self).__init__(dim, folder, inversion_recovery_t1, bounds)
        self.load()

    def load(self):
        """
        load dicom images and TI times
        """
        if self.dim == 2 or 3:
            echos = glob(self.folder + r'\\*\\')
            dcm_files = [get_dcm_list(echo) for echo in echos]
            dcm_files_flatted = [item for sublist in dcm_files for item in sublist]
            dcm_files = split_dcm_List(dcm_files_flatted, True)
            order = self.get_ti(dcm_files)
        else:
            raise UserWarning
        # self.array == echos, z, x, y --> echos, x, y, z
        self.array = np.array([get_dcm_array(dcm_files[o]) for o in order]).transpose(0, 3, 2, 1)

    def get_ti(self, dcm_files):
        """
        Reads TI times from the dicom headers

        Args:
            dcm_files (List): list with all dicom files
        """
        x = []
        for dcm in dcm_files:
            info = pydicom.dcmread(dcm[0])
            x.append(info.InversionTime)
        self.x = np.array([float(te) for te in x])
        order = np.argsort(self.x)
        self.x.sort()
        return order
