from Utilitis import save_nii, get_nan_fitmap
import numpy as np
import csv
import scipy.io


def save_mtr_asym(self):
    save_nii(self.mtr_asym_img, self.mask['affine'], self.mask['header'], self.cest_folder + '/Map.nii.gz')
    scipy.io.savemat(self.cest_folder + '/Map.mat', {'map': self.mtr_asym_img, 'dicom': self.array})
    results = {}
    for i in range(1, int(self.mask['mask'].max()) + 1):
        m, fit_map = get_nan_fitmap(self.mtr_asym_img.copy(), self.mask['mask'].copy(), i)
        results[str(i)] = ['%.2f' % np.nanmean(fit_map), '%.2f' % np.nanstd(fit_map),
                           '%.2f' % np.nanmin(fit_map), '%.2f' % np.nanmax(fit_map),
                           '%.2f' % np.sum(m)]
    with open(self.cest_folder + '_results.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['mask_index', 'mean', 'std', 'min', 'max', 'Pixels'])
        for key, value in results.items():
            value = [v.replace('.', ',') for v in value]
            writer.writerow([key] + value)


def save_lorenzian(self):
    for key in self.lorenzian.keys():
        save_nii(self.lorenzian[key], self.mask['affine'], self.mask['header'],
                 self.cest_folder + '/{}_Map.nii.gz'.format(key))
        scipy.io.savemat(self.cest_folder + '/Lorenzian.mat', self.lorenzian)
        results = {}
        for i in range(1, int(self.mask['mask'].max()) + 1):
            m, fit_map = get_nan_fitmap(self.lorenzian[key].copy(), self.mask['mask'].copy(), i)
            results[str(i)] = ['%.2f' % np.nanmean(fit_map), '%.2f' % np.nanstd(fit_map),
                               '%.2f' % np.nanmin(fit_map), '%.2f' % np.nanmax(fit_map),
                               '%.2f' % np.sum(m)]
        with open(self.cest_folder + '_lorenzian_{}_results.csv'.format(key), mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(['mask_index', 'mean', 'std', 'min', 'max', 'Pixels'])
            for key, value in results.items():
                value = [v.replace('.', ',') for v in value]
                writer.writerow([key] + value)