class CESTConfig:
    def __init__(self, itp_step: float = 0.01,
                 wassr_offset: float = 1.0,
                 max_wassr_shift: float = 0.8,
                 cest_offset: float = 3.0,
                 MTRasym_bool: bool = True,
                 f_shift: float = 1.0,
                 d_shift: float = 1.0,
                 Lorenzian_bool: bool = True,
                 Lorenzian: dict = None,
                 ):

        #########################################################################
        ############################## Interpolation ############################
        #########################################################################
        self.itp_step = itp_step
        self.interpolation = 'quadratic' #cubic, quadratic

        #########################################################################
        ############################## config WASSR #############################
        #########################################################################
        self.wassr_offset = wassr_offset
        self.max_wassr_shift = max_wassr_shift

        #########################################################################
        ############################## config CEST ##############################
        #########################################################################
        self.cest_offset = cest_offset
        self.cest_range = self.cest_offset - self.max_wassr_shift

        #########################################################################
        ########################### config Evaluation ###########################
        #########################################################################

        # MTRasym
        self.MTRasym_bool = MTRasym_bool
        self.MTRasym = {
            'f_shift': f_shift,
            'd_shift': d_shift,
        }

        # Lorenzian (QUELLEN SUCHEN !!!)
        self.Lorenzian_bool = Lorenzian_bool
        self.Lorenzian = {
            'MT_f': - 2.43,
            'NOE1_f': - 1,
            'NOE2_f': - 2.6,
            'OH_f':  1.0, # 1.4,
            'NH_f': + 3.2
        }
        self.lorenzian_keys = ['OH_a', 'OH_w', 'NH_a', 'NH_w']
