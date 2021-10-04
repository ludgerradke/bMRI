from Fitting import T1rho


if __name__ == '__main__':

    # T1rho
    T1rho_folder = r'C:\Users\ludge\Desktop\MRTC-STUDIE_HOCKEY_KNIE_TEST01_MRTC210701\CORE_FACILITY_HOCKEY_ABRAR_20210701_100528_890000_translated\T1rho'
    t1rho = T1rho(dim=3, folder=T1rho_folder, bounds=([0.9, 20, -0.2], [4, 100, 0.00]),
                  config={"TR": 3500, "alpha": 20, "T1": 800})
    t1rho.load_mask()
    t1rho.run(False, [0, 20, 40, 60])
