from Fitting import T1rho, T2_T2star, T1
from CEST import CEST, CESTConfig
from Utilitis import load_nii
import numpy as np

if __name__ == '__main__':

    # T1
    T1_folder = r'E:\ProjekteStudenten\AltersStudieFinger\Messungen\MCP3\DICOM_translated\T1'
    t1 = T1(dim=3, folder=T1_folder, bounds=([-np.inf, 200, -np.inf], [np.inf, 1500, np.inf]))
    t1.load_mask()
    t1.run()

    # T2star
    T2star_folder = r'E:\ProjekteStudenten\AltersStudieFinger\Messungen\MCP3\DICOM_translated\23_T2-star_map_3D_22442'
    t2star = T2_T2star(dim=3, folder=T2star_folder, bounds=None)
    t2star.load_mask()
    t2star.run(multiprocessing=True)

    # T1rho
    T1rho_folder = r'E:\ProjekteStudenten\AltersStudieFinger\Messungen\MCP3\DICOM_translated\T1rho'
    t1rho = T1rho(dim=3, folder=T1rho_folder, bounds=([0.9, 0, -0.05], [1, 70, 0.05]),
                  config={"T1": 800, "TR": 3500, "alpha": 15})
    t1rho.load_mask()
    t1rho.run([0, 5, 15, 25, 35, 45, 55])

    # T2
    T2_folder = r'E:\ProjekteStudenten\AltersStudieFinger\Messungen\MCP3\DICOM_translated\T2'
    t2 = T2_T2star(dim=3, folder=T2_folder, bounds=([0.9, 0, -0.2], [4, 70, 0.05]),
                   config={"T1": 800, "TR": 3500, "alpha": 15, "TE": 6.78, "T2star": 10})
    t2.load_mask()
    t2.run([0, 10, 20, 30, 40, 50, 60])

    # CEST
    CEST_folder = r'E:\ProjekteStudenten\AltersStudieFinger\Messungen\MCP3\DICOM_translated\25_N8PD300B1_05_23493'
    WASSR_foder = r'E:\ProjekteStudenten\AltersStudieFinger\Messungen\MCP3\DICOM_translated\27_WASSR_23833'
    config = CESTConfig(wassr_offset=3)
    cest = CEST(config=config, cest_folder=CEST_folder, wassr_folder=CEST_folder)
    cest.load_mask()
    cest.run()
