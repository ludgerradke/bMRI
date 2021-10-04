from Fitting import T1rho, T2_T2star, T1
from CEST import CEST, CESTConfig
from Utilitis import load_nii
import numpy as np
from glob import glob

if __name__ == '__main__':

    # CEST
    mask, affine, header = load_nii(r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS07\DICOM_translated\2D_CEST_SL\
    90_WASSR_SL_05129\mask.nii.gz')
    CEST_folders = glob(r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS07\DICOM_translated\2D_CEST_SL\*CEST*\\')
    for CEST_folder in CEST_folders:
        CEST_folder = CEST_folder[:-1]
        WASSR_foder = r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS07\DICOM_translated\2D_CEST_SL\90_WASSR_SL_05129'
        config = CESTConfig(cest_offset=5, wassr_offset=1, max_wassr_shift=2, Lorenzian_bool=False)
        cest = CEST(config=config, cest_folder=CEST_folder, wassr_folder=WASSR_foder)
        cest.set_mask(mask, affine, header)
        cest.run()
