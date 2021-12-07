import matplotlib.pyplot as plt
import numpy as np

def rotate_img(img):
    return np.rot90(img)[::-1]

def overlay_dicom_map(d_img, map_img, colorbar_range, file_name):
    d_img = rotate_img(d_img)
    map_img = rotate_img(map_img)
    plt.imshow(map_img, cmap='jet', interpolation='none')
    plt.colorbar()
    plt.clim(colorbar_range[0], colorbar_range[1])
    plt.imshow(d_img, cmap='gray', interpolation='none')
    map_img[map_img == 0.0] = 'nan'
    plt.imshow(map_img, cmap='jet', interpolation='none', alpha=0.5)
    plt.axis('off')
    plt.clim(colorbar_range[0], colorbar_range[1])
    plt.savefig(file_name, bbox_inches='tight')

    plt.close()
