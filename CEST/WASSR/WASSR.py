from CEST.WASSR.MSA import MSA
from CEST.Utils import load_cest_directory, get_ppms
import numpy as np

algorithms = {
    'msa': MSA
}


class WASSR:

    def __init__(self, config, algoritm, dyn=None, *args, **kwargs):
        self.max_offset = config.wassr_offset
        self.algoritm = algorithms[algoritm](config, *args, **kwargs)
        self.offset_map = None
        self.dyn = dyn

    def calculate(self, wassr_directory, mask):
        wassr_img, _ = load_cest_directory(wassr_directory + '/')
        (dyn, rows, colums, z_slices) = wassr_img.shape
        OF = np.zeros((rows, colums, z_slices))

        step_size = (self.max_offset * 2) / (dyn - 1)
        if self.dyn is None:
            ppms = np.arange(-self.max_offset, self.max_offset, step_size).transpose()
            ppms = np.append(ppms, self.max_offset)
        else:
            ppms = np.array(get_ppms(offset=self.max_offset, dyn=self.dyn, directory=wassr_directory))

        pixels = np.argwhere(mask != 0)

        for i, tuple in enumerate(pixels):
            values = wassr_img[:, tuple[0], tuple[1], tuple[2]]
            OF[tuple[0], tuple[1], tuple[2]] = self.algoritm.calculate(ppms, values)
        self.offset_map = OF
        mask[self.offset_map == -100] = 0
        return self.offset_map, mask
