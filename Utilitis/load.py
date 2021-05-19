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
    for key in locations.keys():
        for idx in range(len(echo_list)):
            echo_list[idx].append(locations[key][idx])
    if sort:
        return sort_echo_list(echo_list)
    return echo_list


def sort_echo_list(echos: list):
    sort_echos, sort_echos_alternative = [], []
    for _ in range(len(echos)):
        sort_echos.append('')
    for echo in echos:
        sort_echo = []
        for _ in echo:
            sort_echo.append('')
        for f in echo:
            d = pydicom.dcmread(f)
            try:
                sort_echo[int(d.InstanceNumber)-1] = f
            except IndexError:
                sort_echo[0] = f
        sort_echos[int(d.AcquisitionNumber) - 1] = sort_echo
        sort_echos_alternative.append((sort_echo, d.SeriesNumber))
    if '' in sort_echos:
        sort_echos = sorted(sort_echos_alternative, key=lambda tup: tup[1])
        sort_echos = [tup[0] for tup in sort_echos]
    return sort_echos


def get_dcm_array(data: list):
    array = []
    for d in data:
        img = pydicom.dcmread(d).pixel_array
        info = pydicom.dcmread(d)
        #try:
        #    img = img * info.RescaleSlope + info.RescaleIntercept
        #except AttributeError:
         #   pass
        array.append(img)
    array = array[::-1]
    return np.array(array)


def load_nii(file):
    nimg = nib.load(file)
    return nimg.get_fdata(), nimg.affine, nimg.header
