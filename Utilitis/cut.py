from scipy.ndimage import zoom


def resize_mask_array(mask, array):
    mask, array = cut_mask_and_array(mask, array)
    if mask.shape[-2] != array.shape[-2]:
        x, y = array.shape[-3] / mask.shape[-2], array.shape[-3] / mask.shape[-2]
        z = 1
        mask = zoom(mask, (x, y, z), mode='nearest')

    return mask.round(), array


def cut_mask_and_array(mask, array):
    if mask.shape[-1] < array.shape[-1]:
        cut = round((array.shape[-1] - mask.shape[-1]) / 2)
        array = array[:, :, :, cut:-cut]
    elif mask.shape[-1] > array.shape[-1]:
        cut = round((mask.shape[-1] - array.shape[-1]) / 2)
        mask = mask[:, :, cut:-cut]
    return mask, array