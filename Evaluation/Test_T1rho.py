from Fitting import T1rho, T2_T2star, T1
from CEST import CEST, CESTConfig
import numpy as np

if __name__ == '__main__':

    # T1
    # T1_folder = r'D:\Test_T1rho_translated\T1'
    #t1 = T1(dim=3, folder=T1_folder, bounds=([0, 200, -1], [np.inf, 2500, 0]))
    #t1.load_mask()
    #t1.run(True)
    #t1_map = t1.get_map()

    # T1rho
    T1rho_folder = r'D:\MRTC_TEST210625_TEST_MRTC_TEST_210625\CORE_FACILITY_HOCKEY_ABRAR_20210625_082725_218000_translated'
    t1rho = T1rho(dim=3, folder=T1rho_folder, bounds=([0.9, 0, -0.2], [4, 70, 0.05]),
                  config={"TR": 3500, "alpha": 15, "T1": 1500})
    t1rho.load_mask()
    t1rho.run(False, [0, 30, 100])

    # T2
    T2_folder = r'D:\Test_T1rho_translated\T2_TR_3500'
    t1rho = T1rho(dim=3, folder=T2_folder, bounds=([0.9, 0, -0.2], [4, 70, 0.05]),
                  config={"TR": 3500, "alpha": 15, "T1": 1500})
    t1rho.load_mask()
    t1rho.run(False, [0, 15, 30, 45, 60])

    # T1rho
    T1rho_folder = r'D:\Test_T1rho_translated\T1rho_TR_500'
    t1rho = T1rho(dim=3, folder=T1rho_folder, bounds=([0.9, 0, -0.2], [4, 70, 0.05]),
                  config={"TR": 500, "alpha": 15, "T1": 1500})
    t1rho.load_mask()
    t1rho.run(False, [0, 15, 30, 45, 60])

    # T2
    T2_folder = r'D:\Test_T1rho_translated\T2_TR_500'
    t1rho = T1rho(dim=3, folder=T2_folder, bounds=([0.9, 0, -0.2], [4, 70, 0.05]),
                  config={"TR": 500, "alpha": 15, "T1": 1500})
    t1rho.load_mask()
    t1rho.run(False, [0, 15, 30, 45, 60])