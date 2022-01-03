import pydicom
from glob import glob
import numpy as np
import nibabel as nib
import os
from PIL import Image, ImageDraw


def get_dcm_list(folder: str):
    dcm_list = sorted(glob(folder + os.sep + '*.dcm'))
    #if len(dcm_list) == 0:
    #    return sorted(glob(folder + '\*'))
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


def transform_gui_segmentation_to_nii(path):
    DicomList = sorted(glob(path + '/*.dcm'))

    shape = pydicom.dcmread(DicomList[0]).pixel_array.astype(np.uint8).shape[0]
    OverAllMaske = np.zeros([len(DicomList), shape, shape])
    for k in range(len(DicomList)):
        loadFileNameMain = DicomList[k]
        loadFileName = loadFileNameMain[:-4] + '_poly.txt'
        try:
            loadFile = open(loadFileName, 'r')
        except FileNotFoundError:
            continue
        File = np.genfromtxt(loadFile, delimiter=',')
        File = np.nan_to_num(File)
        length = len(File)
        for i in range(length):
            PolyList = []
            for j in range(100):
                try:
                    x = File[i][j * 2]
                    y = File[i][j * 2 + 1]
                except IndexError:
                    x = File[j * 2]
                    y = File[j * 2 + 1]
                if x == 0 or x == 2000:
                    break
                PolyList.append((x, y))
            if len(PolyList) > 2:
                img = Image.new('L', (int(shape), int(shape)), 0)
                ImageDraw.Draw(img).polygon(PolyList, outline=1, fill=1)
                array = (i + 1) * np.array(img)
                array[OverAllMaske[k, :, :] != 0] = 0
                OverAllMaske[k, :, :] += array
    return OverAllMaske
