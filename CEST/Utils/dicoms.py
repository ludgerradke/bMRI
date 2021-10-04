import numpy as np
from Utilitis import get_dcm_list, split_dcm_List, get_dcm_array
from scipy.ndimage import gaussian_filter
import pydicom


def load_cest_directory(directory):
    dcm_files = get_dcm_list(directory)
    dcm_files = split_dcm_List(dcm_files)
    array = np.array([get_dcm_array(dcm) for dcm in dcm_files]).transpose(0, 3, 2, 1).astype(np.float)
    array = cest_gaussian_filter(array, 1, '2D')
    array_normalize = normalize(array)
    return array_normalize, array


def normalize(array):
    np.seterr(divide='ignore', invalid='ignore')
    zero_img = array[0, :, :, :]
    array = array[1:, :, :, :]
    for i in range(array.shape[0]):
        img = array[i, :, :, :]
        img = img / zero_img
        nan_elems = np.isnan(img)
        img[nan_elems] = 0.0
        inf_elems = np.isinf(img)
        img[inf_elems] = 0.0
        array[i, :, :, :] = img
    return array


def cest_gaussian_filter(array, sigma, mode):
    if mode is None:
        return array
    if mode == '2D':
        for i in range(array.shape[0]):
            for j in range(array.shape[-1]):
                array[i, :, :, j] = gaussian_filter(array[i, :, :, j], sigma)
    if mode == '3D':
        array = gaussian_filter(array, sigma)
    return array


def get_ppms(offset, dyn, directory):
    dcm_files = get_dcm_list(directory)
    dcm_files = split_dcm_List(dcm_files)
    step_size = (offset * 2) / (dyn - 1)
    ppm = np.arange(-offset, offset, step_size).transpose()
    ppm = np.append(ppm, offset)
    if int(pydicom.dcmread(dcm_files[0][0]).AcquisitionNumber) == 1:
        dcm_files = dcm_files[1:]
        ppm_list = [ppm[int(pydicom.dcmread(f[0]).AcquisitionNumber)-1]for f in dcm_files]
        return ppm_list
    ppm_list = [ppm[int(pydicom.dcmread(f[0]).AcquisitionNumber) - 1] for f in dcm_files]
    return ppm_list[1:]

if __name__ == '__main__':
    offset = 6
    dyn = 512
    directory = r'D:\Klinik Projekte\19_Anja_Niere_CEST\TEST_Messungen\CESTDataM_FilterFFT_rect\CESTDataM_FilterFFT_rect'
    get_ppms(offset, dyn, directory)