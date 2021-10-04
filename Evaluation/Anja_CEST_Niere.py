from Fitting import T1rho, T2_T2star, T1
from CEST import CEST, CESTConfig
from Utilitis import load_nii
import numpy as np

if __name__ == '__main__':

    # CEST
    CEST_folder = r'D:\Klinik Projekte\19_Anja_Niere_CEST\TEST_Messung_with_S0\CESTDataM_FilterFFT_S0_in'
    WASSR_foder = r'D:\Klinik Projekte\19_Anja_Niere_CEST\TEST_Messung_with_S0\WASSRData_FilterFFT_S0_in'
    config = CESTConfig(wassr_offset=1, cest_offset=6)
    cest = CEST(config=config, cest_folder=CEST_folder, wassr_folder=WASSR_foder, dyn_wassr=102, dyn_cest=512)
    mask, affine, header = load_nii(r'D:\Klinik Projekte\19_Anja_Niere_CEST\TEST_Messung_with_S0\mask.nii.gz')
    cest.set_mask(mask, affine, header)
    cest.run()
