from Utilitis import overlay_dicom_map, load_nii, save_nii, resize_mask_array
import numpy as np
from scipy.optimize import curve_fit
from abc import ABC, abstractmethod
import csv, os
from multiprocessing import Pool


class AbstractFitting(ABC):
    """
    Abstracted class that provides the essential functions for the various fit classes.

    Args:
        dim (int): Dimension of the images (2 or 3D)

        folder (str): path to the dicom images, here it is to be noted that in the derived classes
            the function fit is implemented, depending on the respective implementation the path must be
            passed correctly

        fit_funktion (*function): Pointer to the respective fit function

        bounds (tuple([len(n)], [len(n)]): Bounds values of the fit function bounds = ([x_min, y_min, z_min],
            [x_max, y_max, z_max]).
            Note: The bounds are handed in according to the scipy.optimize.curve_fit convention.
    """

    def __init__(self, dim, folder, fit_function, bounds=None, config_fit=None):
        self.dim = dim
        self.folder = folder
        self.bounds = bounds
        self.x = None
        self.mask = None
        self.fit_map = None
        self.r_squares = None
        self.array = None
        self.fit_function = fit_function
        self.sort = False
        self.config_fit = config_fit

    @abstractmethod
    def load(self):
        pass

    def load_mask(self):
        """
        Automatic import of the mask, it is assumed that the mask is in the same path as the commit path
            (see init function: folder). The file must be named as mask.nii.gz!
        Args:
            None

        Returns:
            None
        """
        mask, affine, header = load_nii(self.folder + r'\mask.nii.gz')
        self.set_mask(mask, affine, header)

    def set_mask(self, mask, affine, header):
        """
        set mask manual

        Args:
            mask (np.array): Integer Array, hierbei entspricht jede Zahl einer segmentiereten Klasse
            affine (np.array): An array that tells you the position of the image array data in a reference space.
            header (): image metadata (data about the data) describing the image, usually in the form of an image header

        Returns:
            None
        """
        self.mask = {
            'mask': mask,
            'affine': affine,
            'header': header
        }

    def get_map(self):
        return self.fit_map

    def run(self, multiprocessing=False, x=None):
        """
        Starts the essential functions
        """
        self.fit(multiprocessing, x)
        self.overlay_map()
        return self.save_results()

    def fit(self, multiprocessing=False, x=None):
        """
        Calculates the fit_map (array in the image dimension where the fitted times are stored).

        Args:
            x (np.array): times of the different acquisitions. If x = None, it is assumed that the times could be
                read out from the dicom header when importing the image.

        Returns:
            fit_map (np.array): array with the fitted times (T1, T2, T2star, .....)

        Note: It is important that the data and the array have already been read in beforehand. The quality of the fits
            (R^2) is saved as a class variable, but not returned.
        """
        x = self.x if x is None else x
        mask = self.mask['mask']
        if x is None or mask is None:
            return
        assert self.array.shape[0] == len(x), 'The passed times: {} do not match the dimension ({}) of the ' \
                                              'loaded Dicom files!!'.format(x, self.array.shape[0])
        mask, self.array = resize_mask_array(mask, self.array)
        self.mask['mask'] = mask
        fit_map = np.zeros(mask.shape)
        r_squares = np.zeros(mask.shape)

        if multiprocessing:
            with Pool() as pool:
                idxs, map, r_square = zip(*pool.map(fit_slice_process,
                                                    [(fit_map[:, :, i], r_squares[:, :, i], self.array[:, :, :, i],
                                                      mask[:, :, i],
                                                      x, self.fit_function, self.bounds, i, self.config_fit[:, :, i] if
                                                      self.config_fit is not None else None) for i in
                                                     range(self.array.shape[-1])]))
                for i in range(len(idxs)):
                    fit_map[:, :, idxs[i]], r_squares[:, :, idxs[i]] = map[idxs[i]], r_square[idxs[i]]
        else:
            for i in range(self.array.shape[-1]):
                config_fit = None if self.config_fit is None else self.config_fit[:, :, i]
                fit_map[:, :, i], r_squares[:, :, i] = fit_slice(self.array[:, :, :, i], mask[:, :, i],
                                                                 x, self.fit_function, self.bounds, config_fit)

        self.fit_map = fit_map
        self.r_squares = r_squares
        return fit_map

    def overlay_map(self, fit_map=None):
        """
        Overlays and saves the calculated map

        Args:
            fit_map (np.array): map to overlay, if fit_map = None, then it is assumed that the map was
                previously calculated and therefore stored in self.fit_map
        Outputs:
            map_dyn_{03d}.format(i): Overlaid images saved as .png
        """
        fit_map = self.fit_map if fit_map is None else fit_map
        clim = np.nanmax(fit_map)
        for i in range(fit_map.shape[-1]):
            file = self.folder + r'\map_dyn_{:03d}.png'.format(i)
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
            if np.nanmax(fit_map[:, :, i]) > 0:
                overlay_dicom_map(self.array[0, :, :, i], fit_map[:, :, i], [0, clim], file)

    def save_results(self):
        """
        Saves the calculated results.

        Output:
            Map.nii.gz : Calculated results as nii array, can be visualized e.g. with ITK-Snap or overlaid on the images
                in the following adapted with other functions.
            _results.csv: CSV file in which for each class separately mean, standard deviation, minimum, maximum and
                number of pixels is calculated.
        """
        save_nii(self.fit_map, self.mask['affine'], self.mask['header'], self.folder + '/Map.nii.gz')
        results = {}
        for i in range(1, int(self.mask['mask'].max()) + 1):
            m = self.mask['mask'].copy()
            m = np.where(m == i, 1, 0)

            fit_map = np.multiply(self.fit_map, m)
            fit_map = np.where(fit_map != 0.0, fit_map, np.nan)

            r_squares = np.multiply(self.r_squares, m)
            r_squares = np.where(r_squares != 0, r_squares, np.nan)

            results[str(i)] = ['%.2f' % np.nanmean(fit_map), '%.2f' % np.nanstd(fit_map),
                               '%.2f' % np.nanmin(fit_map), '%.2f' % np.nanmax(fit_map),
                               '%.2f' % np.sum(m), '%.2f' % np.nanmean(r_squares)]
        with open(self.folder + '_results.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(['mask_index', 'mean', 'std', 'min', 'max', 'Pixels', 'Mean R^2'])
            for key, value in results.items():
                value = [v.replace('.', ',') for v in value]
                writer.writerow([key] + value)
        return results


def fit_slice_process(data):
    data = list(data)
    data[0], data[1] = fit_slice(data[2], data[3], data[4], data[5], data[6], config_fit=data[8], min_r_squared=0.1)
    return data[7], data[0], data[1]


def fit_slice(d_slice, mask, x, fit, bounds, config_fit = None, min_r_squared=0):
    bounds_ = ([bounds[0][0], 0.9 * bounds[0][1], bounds[0][2]],
                     [bounds[1][0], 1.1 * bounds[1][1], bounds[1][2]])
    """
    Fits one slice

    Args:
        d_slice (np.array): dicom array [times, rows, columns].
        mask (np.array): [Rows, Columns].
        x (list): list with the different time points ([time_1, time_2, time_3, time_4, ...])
        fit (*function): Pointer to the respective fit function
        bounds (tuple([len(n)], [len(n)]): Bounds values of the fit function bounds = ([x_min, y_min, z_min],
            [x_max, y_max, z_max]).
            Note: The bounds are handed in according to the scipy.optimize.curve_fit convention.
        min_r_squared (float): Grenzwert über dem R^2 liegen muss, damit der Pixel eingeschlossen wurde.

    Returns:
        fit_map (np.array): array with the fitted times (T1, T2, T2star, .....)
        r_squares (np.array): array with the calculated r_squares
    """
    fit_map = np.full((d_slice.shape[1], d_slice.shape[2]), np.nan)
    r_squares = fit_map.copy()
    if mask.max() == 0:
        return fit_map, r_squares

    args = np.argwhere(mask != 0)
    for row, column in args:
        y = d_slice[:, row, column]
        try:
            y = y / y.max()
        except ValueError:
            continue
        try:
            if config_fit is not None:
                fit_ = fit((config_fit[row, column]))
            else:
                fit_ = fit
            if bounds is not None:
                param, param_cov = curve_fit(fit_, x, y, bounds=bounds_, xtol=0.1, maxfev=400)
            else:
                param, param_cov = curve_fit(fit_, x, y, xtol=0.1)
        except RuntimeError:
            continue
        except ValueError:
            continue
        residuals = y - fit_(np.array(x), param[0], param[1], param[2])
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        if r_squared < min_r_squared:
            continue
        if param[1] <= bounds[0][1] or param[1] >= bounds[1][1]:
            continue
        fit_map[row, column] = param[1]
        r_squares[row, column] = r_squared
    return fit_map, r_squares
