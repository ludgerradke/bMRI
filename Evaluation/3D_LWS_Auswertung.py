from Fitting import T1rho, T2_T2star, T1
from CEST import CEST, CESTConfig
from Utilitis import load_nii
import numpy as np
from glob import glob

if __name__ == '__main__':

    # CEST
    mask, affine, header = load_nii(r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS06\DICOM_translated\2D CEST SL\69_WASSR_B1_0,2_tp_50k_12858\Mask.nii.gz')
    CEST_folders = glob(r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS06\DICOM_translated\2D CEST SL\*CEST*')
    for CEST_folder in CEST_folders:
        WASSR_foder = r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS06\DICOM_translated\2D CEST SL\69_WASSR_B1_0,2_tp_50k_12858'
        config = CESTConfig(cest_offset=3.66, wassr_offset=1, Lorenzian_bool=False)
        cest = CEST(config=config, cest_folder=CEST_folder, wassr_folder=CEST_folder)
        cest.set_mask(mask, affine, header)
        cest.run()
