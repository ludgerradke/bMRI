from Fitting import T1rho, T2_T2star
from Utilitis import load_nii
from glob import glob
if __name__ == '__main__':


    # T1rho
    T1rho_folder = r'D:\Klinik Projekte\18_Hockey\Messung_1\01\DICOM\AA4F8D87_translated\T1rho'
    mask, affine, header = load_nii(r'D:\Klinik Projekte\18_Hockey\Messung_1\01\DICOM\AA4F8D87_translated\Mask_T1rho.nii.gz')
    mask[mask > 2] = 0
    t1rho = T1rho(dim=3, folder=T1rho_folder,  bounds=([0.8, 20, -0.2], [1.1, 100, 0.05]),
                  config={"TR": 3500, "alpha": 15, "T1": 800})
    t1rho.set_mask(mask, affine, header)
    #t1rho.load_mask()
    #t1rho.run(False, [0, 10, 40, 70])

    # T2
    T2_folder = r'D:\Klinik Projekte\18_Hockey\Messung_1\01\DICOM\AA4F8D87_translated\14_T2_map_48slc_07097'
    mask, affine, header = load_nii(
        r'D:\Klinik Projekte\18_Hockey\Messung_1\01\DICOM\AA4F8D87_translated\Mask_T1rho.nii.gz')
    mask[mask > 2] = 0
    t2 = T2_T2star(dim=3, folder=T2_folder,  bounds=([0.8, 20, -0.2], [1.2, 80, 0.5]))
    t2.set_mask(mask, affine, header)
    #t1rho.load_mask()
    t2.run(False)
