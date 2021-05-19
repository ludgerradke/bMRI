import numpy as np
from Utilitis import get_dcm_list, split_dcm_List, get_dcm_array


def load_cest_directory(directory):
    dcm_files = get_dcm_list(directory)
    dcm_files = split_dcm_List(dcm_files)
    array = np.array([get_dcm_array(dcm) for dcm in dcm_files]).transpose(0, 3, 2, 1).astype(np.float)
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
