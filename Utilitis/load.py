import pydicom
from glob import glob
import numpy as np
import nibabel as nib


def get_dcm_list(folder: str):
    dcm_list = sorted(glob(folder + '*.dcm'))
    return dcm_list


def split_dcm_List(dcm_list: list, sort=False):
    locations = {}
    for f in dcm_list:
        try:
            d = pydicom.dcmread(f)
        except BaseException:
            continue
        if d['SliceLocation'].value in locations.keys():
            locations[d['SliceLocation'].value].append(f)
        else:
            locations[d['SliceLocation'].value] = [f]
    split_dcmList = [locations[key] for key in locations.keys()]
    echo_list = [[] for i in range(len(split_dcmList[0]))]
    keys = list(locations.keys())
    keys.sort()
    for key in keys:
        echos = locations[key]
        echos = sort_echo_list(echos)
        for idx in range(len(echo_list)):
            echo_list[idx].append(echos[idx])
    return echo_list


def sort_echo_list(echos: list):
    InstanceNumbers = [int(pydicom.dcmread(file).InstanceNumber) for file in echos]
    SeriesNumbers = [int(pydicom.dcmread(file).SeriesNumber) for file in echos]

    # remove duplicates
    InstanceNumbers = list(dict.fromkeys(InstanceNumbers))
    SeriesNumbers = list(dict.fromkeys(SeriesNumbers))
    if len(InstanceNumbers) > 1:
        order = np.argsort(InstanceNumbers)
    elif len(SeriesNumbers) > 1:
        order = np.argsort(SeriesNumbers)
    else:
        print("Warning: Sorting not possible!")
        return echos

    sort_echos = [echos[o] for o in order]
    return sort_echos


def get_dcm_array(data: list):
    array = []
    for d in data:
        img = pydicom.dcmread(d).pixel_array
        info = pydicom.dcmread(d)
        try:
            img = img * info.RescaleSlope + info.RescaleIntercept
        except AttributeError:
            pass
        array.append(img)
    array = array[::-1]
    return np.array(array)


def load_nii(file):
    nimg = nib.load(file)
    return nimg.get_fdata()[:, :, ::-1], nimg.affine, nimg.header
