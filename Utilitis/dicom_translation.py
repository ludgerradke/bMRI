import os
import re
import shutil
import sys
from PyQt5.QtWidgets import QFileDialog
import pydicom
from PyQt5.QtWidgets import *


def extract_series(ds):
    SeriesDescription = re.sub(':', '', ds.SeriesDescription)
    SeriesInstanceUID = ds.SeriesInstanceUID.split('.0.0', 1)[0][-5:]
    return str(SeriesDescription + '_' + SeriesInstanceUID)


def create_directory_list(path):
    lstDirsDCM = []
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for subdir in subdirList:
            lstDirsDCM.append(os.path.join(dirName, subdir))
    return lstDirsDCM


def rename_dicom_file(ds, oldFilename):
    AcquisitionNumber = 0
    InstanceNumber = 0
    Series = 0
    if 'AcquisitionNumber' in ds:
        AcquisitionNumber = ds.AcquisitionNumber
    if 'InstanceNumber' in ds:
        InstanceNumber = ds.InstanceNumber
    if 'SeriesNumber' in ds:
        Series = ds.SeriesNumber
    if InstanceNumber < 10:
        SL = '000' + str(InstanceNumber)
    elif InstanceNumber < 100:
        SL = '00' + str(InstanceNumber)
    elif InstanceNumber < 1000:
        SL = '0' + str(InstanceNumber)
    else:
        SL = str(InstanceNumber)

    newFilename = os.path.join(PathResult,
                               str(Series) + '_' + extract_series(ds),
                               extract_series(ds) + '_dyn_' +
                               SL + '.dcm')
    shutil.copyfile(oldFilename, newFilename)


def copy_file(fileDCM):
    try:
        ds = pydicom.dcmread(fileDCM)
        rename_dicom_file(ds, fileDCM)
    except pydicom.errors.InvalidDicomError:
        print('The file ' + fileDCM + ' is not a DICOM file')
        pass
    except IsADirectoryError:
        print('The file ' + fileDCM + ' is a directory')
        pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass


def sort_dicom_files(lstDirsDCM):
    for dirnameDCM in lstDirsDCM:
        for fileDCM in os.listdir(dirnameDCM):
            copy_file(os.path.join(dirnameDCM, fileDCM))


def create_series_set(lstDirsDCM):
    seriesSet = set()
    for dirnameDCM in lstDirsDCM:
        for fileDCM in os.listdir(dirnameDCM):
            try:
                ds = pydicom.dcmread(os.path.join(dirnameDCM, fileDCM))
                series = str(ds.SeriesNumber) + '_' + extract_series(ds)
                seriesSet.add(series)
            except:
                print('The file ' + fileDCM + ' is not a DICOM file')
                print("Unexpected error:", sys.exc_info()[0])
                pass
    return seriesSet


def prepare_destinations(seriesSet, path):
    if not os.path.isdir(os.path.join(path)):
        os.mkdir(path)

    for serie in seriesSet:
        shutil.rmtree(os.path.join(path, serie), ignore_errors=True)
        os.mkdir(os.path.join(path, serie))


def load_dicom_files():
    print('Sort DICOM files')
    dirList = create_directory_list(PathDicom)
    seriesSet = create_series_set(dirList)
    prepare_destinations(seriesSet, PathResult)
    sort_dicom_files(dirList)
    print('Done')


def load_dicom_filesExtern(PathDicomParameter, PathResultParameter):
    global PathDicom
    global PathResult
    PathDicom = PathDicomParameter
    PathResult = PathResultParameter
    dirList = create_directory_list(PathDicom)
    seriesSet = create_series_set(dirList)
    prepare_destinations(seriesSet, PathResult)
    sort_dicom_files(dirList)
    return 'Done'


class filedialogdemo(QWidget):
   def __init__(self, parent = None):
      super(filedialogdemo, self).__init__(parent)


def translation_main():
    path = QFileDialog.getExistingDirectory()
    if path == "":
        return False
    resultpath = path + '_translated'
    if not os.path.isdir(resultpath):
        os.mkdir(resultpath)
    load_dicom_filesExtern(path, resultpath)
    return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    translation_main()
