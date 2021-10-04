from Fitting import T2_T2star
from Utilitis import load_nii
from glob import glob
import numpy as np
import os, csv

if __name__ == '__main__':
    seg_folder = r'D:\Klinik Projekte\16_Loading_Sven\Segmentierungen DESS'
    segmentations = glob(seg_folder + '/*T2resliced.nii*')

    data_folder = r'D:\Klinik Projekte\16_Loading_Sven\KnieLoadingProbandender'

    probanden = glob(data_folder + '/*')
    count = 0
    res = []
    dif = []
    for proband in probanden:
        for mode in ["unloaded", "loaded"]:
            T2_folder = glob(proband + '/{}/T2Map*'.format(mode))

            sub = os.path.basename(proband).replace('P0', 'P')
            masks_path = list(filter(None, [seg_string if sub in seg_string else None for seg_string in segmentations]))

            masks_path = list(filter(None, [seg_string if '_' + mode in seg_string else None for seg_string in masks_path]))
            if len(masks_path) != 1:
                continue
            mask, affine, header = load_nii(masks_path[0])
            mask = mask - 2
            mask = np.where(mask < 1, 0, mask)
            # mask = mask[:, :, ::-1]
            mask[:, :, :2] = 0
            mask[:, :, -2:] = 0

            t2 = T2_T2star(dim=3, folder=T2_folder[0], bounds=([1, 20, -0.2], [4, 80, 0.2]))
            t2.set_mask(mask, affine, header)
            t2_res = t2.run(multiprocessing=True)
            print(t2_res)
            res.append([os.path.basename(proband), mode, '1'] + t2_res['1'])
            res.append([os.path.basename(proband), mode, '2'] + t2_res['2'])

    fields = ['Proband', 'Mode', 'mask_index', 'mean', 'std', 'min', 'max', 'Pixels', 'Mean R^2']
    with open(r'D:\Klinik Projekte\16_Loading_Sven\results.csv', mode='w', newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f, delimiter=';')
        write.writerow(fields)
        for line in res:
            line = [v.replace('.', ',') for v in line]
            write.writerow(line)
