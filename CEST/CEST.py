import numpy as np
import os

from CEST.Utils import load_cest_directory, save_lorenzian, save_mtr_asym, get_ppms
from CEST.Evaluation import calc_mtr_asym, cest_correction, calc_lorentzian
from Utilitis import load_nii, resize_mask_array
from Utilitis.overlay import overlay_dicom_map
from CEST.WASSR import WASSR


class CEST:
    def __init__(self, config, cest_folder, wassr_folder, dyn_wassr=None, dyn_cest=None):
        self.cf = config
        self.hStep = config.itp_step
        self.max_offset = config.cest_offset
        self.range = config.cest_range
        self.f_shift = config.MTRasym['f_shift']
        self.d_shift = config.MTRasym['d_shift']
        self.cest_folder = cest_folder
        self.wassr_folder = wassr_folder
        self.CestCurveS = None
        self.x_calcentires = None
        self.interpolation = config.interpolation
        self.dyn_wassr = dyn_wassr
        self.dyn_cest = dyn_cest

    def load_mask(self):
        mask, affine, header = load_nii(self.wassr_folder + r'\mask.nii.gz')
        self.set_mask(mask, affine, header)

    def set_mask(self, mask, affine, header):
        self.mask = {
            'mask': mask,
            'affine': affine,
            'header': header
        }

    def run(self):
        self.wassr_correction()
        self.cest_correction()
        self.calc_lorenzian()
        self.calc_mtr_asym()
        self.overlay_map()
        self.save_results()

    def overlay_map(self, mtr_asym_img=None, lorenzian_img=None):
        if self.cf.MTRasym_bool or mtr_asym_img is not None:
            mtr_asym_img = self.mtr_asym_img if mtr_asym_img is None else mtr_asym_img
            min_ = 0 #int(np.quantile(mtr_asym_img[mtr_asym_img != 0], 0.15))
            max_ = 3 #int(np.quantile(mtr_asym_img[mtr_asym_img != 0], 0.85)) + 1
            for i in range(mtr_asym_img.shape[-1]):
                file = self.cest_folder + r'\mtr_asym_map_dyn_{:03d}'.format(i + 1)
                try:
                    os.remove(file)
                except FileNotFoundError:
                    pass
                if np.nanmax(mtr_asym_img[:, :, i]) > 0:
                    overlay_dicom_map(self.array[0, :, :, i], mtr_asym_img[:, :, i], [min_, max_], file)
        if self.cf.Lorenzian_bool:
            lorenzian_img = self.lorenzian['OH_a'] if lorenzian_img is None else lorenzian_img
            min_ = int(np.quantile(lorenzian_img[lorenzian_img != 0], 0.15)*10)/10
            max_ = (int(np.quantile(lorenzian_img[lorenzian_img != 0], 0.85)*10) + 1)/10
            for i in range(lorenzian_img.shape[-1]):
                file = self.cest_folder + r'\lorenzian_map_dyn_{:03d}'.format(i + 1)
                try:
                    os.remove(file)
                except FileNotFoundError:
                    pass
                if np.nanmax(lorenzian_img[:, :, i]) > 0:

                    overlay_dicom_map(self.array[0, :, :, i], lorenzian_img[:, :, i], [min_, max_], file)

    def calc_mtr_asym(self):
        if self.cf.MTRasym_bool:
            mtr_asym_curves, mtr_asym_img = calc_mtr_asym(self.CestCurveS, self.x_calcentires, self.mask['mask'], self.d_shift,
                                                          self.f_shift, self.hStep)
            self.mtr_asym_curves = mtr_asym_curves
            self.mtr_asym_img = mtr_asym_img

    def calc_lorenzian(self):
        if self.cf.Lorenzian_bool:
            self.lorenzian = calc_lorentzian(self.CestCurveS, self.x_calcentires, self.mask['mask'], self.cf)

    def save_results(self):
        if self.cf.MTRasym_bool:
            save_mtr_asym(self)
        if self.cf.Lorenzian_bool:
            save_lorenzian(self)

    def wassr_correction(self):
        self.cest_array, self.array = load_cest_directory(self.cest_folder + '/')
        wassr = WASSR(self.cf, algoritm='msa', dyn=self.dyn_wassr)
        self.mask['mask'], self.array = resize_mask_array(self.mask['mask'], self.array)
        self.offset_map, self.mask['mask'] = wassr.calculate(self.wassr_folder, self.mask['mask'])

    def load_cest_array(self):
        try:
            cest_array = self.cest_array
        except AttributeError:
            cest_array, self.array = load_cest_directory(self.cest_folder + '/')
        return cest_array

    def cest_correction(self):
        cest_array = self.load_cest_array()
        x_calcentires = np.arange(-self.range, self.range, self.hStep)
        x_calcentires = np.append(x_calcentires, self.range)
        dyn = cest_array.shape[0]
        step_size = (self.max_offset * 2) / (dyn - 1)
        if self.dyn_cest is None:
            x = np.arange(-self.max_offset, self.max_offset, step_size).transpose()
            x = np.append(x, self.max_offset)
        else:
            x = get_ppms(offset = self.cf.cest_offset, dyn = self.dyn_cest, directory=self.cest_folder)

        x_itp = np.arange(-self.max_offset, self.max_offset, self.hStep).transpose()
        x_itp = np.append(x_itp, self.max_offset)

        mask = self.mask['mask']
        self.CestCurveS, self.x_calcentires = cest_correction(cest_array, x_calcentires, x, x_itp, mask,
                                                              self.offset_map, self.interpolation, self.cf.cest_range)
        b = 2
