from Fitting import T1rho, T2_T2star, T1
from CEST import CEST, CESTConfig
from Utilitis import load_nii
import numpy as np
from glob import glob

if __name__ == '__main__':

    # CEST
    mask, affine, header = load_nii(r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS07\DICOM_translated\3D_Messungen\37_WASSR_ORIG_01101\mask.nii.gz')
    CEST_folder = r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS07\DICOM_translated\3D_Messungen\22_CEST_3D_B1_1_ORIG_12797'
    WASSR_foder = r'E:\PhD Projekte\5_gagCEST_LWS\Messungen\LWS07\DICOM_translated\3D_Messungen\37_WASSR_ORIG_01101'
    config = CESTConfig(cest_offset=4, wassr_offset=4, Lorenzian_bool=False)
    cest = CEST(config=config, cest_folder=CEST_folder, wassr_folder=CEST_folder)
    cest.set_mask(mask, affine, header)
    cest.run()
