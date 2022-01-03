import numpy as np


def get_nan_fitmap(fit_map, mask, i):
    mask[mask != i] = 0
    mask[mask == i] = 1
    fit_map = np.multiply(fit_map, mask)
    fit_map = np.where(fit_map != 0.0, fit_map, np.nan)
    return mask, fit_map

def find_slice_shape(ax1, ax2, ax3):
    if ax1 == ax2:
        return 2
    if ax1 == ax3:
        return 1
    return 0

def reform_mask(mask, current_slice_ax):
    if current_slice_ax == 2:
        return mask
    if current_slice_ax == 1:
        return np.transpose(mask, (0, 2, 1))
    return np.transpose(mask, (2, 1, 0))

def transform_mask_with_multiechos(mask, echos):
    shape = mask.shape
    assert len(shape) == 3
    ax1, ax2, ax3 = shape
    current_slice_ax = find_slice_shape(ax1, ax2, ax3)
    mask = reform_mask(mask, current_slice_ax)
    slices = int(mask.shape[-1] / echos)
    out_mask = np.zeros((mask.shape[0], mask.shape[1], slices))
    for i in range(slices):
            out_mask[:, :, i] = mask[:, :, i::slices].max(axis=2)
    return out_mask