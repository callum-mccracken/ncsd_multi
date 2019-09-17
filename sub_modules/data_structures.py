"""contains the Params class and subclasses, which are pretty basic

they have attributes for every field in the data files, e.g. mfdp.dat files
have a field for Z, so a MFDPParams object has an attribute .Z
"""
# all the required/allowed fields for each data structure
min_keys = [
    "mfdp_path", 
    "interactions_directory", 
    "ncsd_path", 
    "two_body_interaction", 
    "Z", 
    "N", 
    "hbar_omega", 
    "N_1max", 
    "N_12max", 
    "N_123max", 
    "three_body_interaction", 
    "Nmax_min", 
    "Nmax_max", 
    "Nmax_IT", 
    "interaction_type", 
    "n_states", 
    "iterations_required", 
    "irest", 
    "nhw_restart", 
    "kappa_points", 
    "kappa_vals", 
    "kappa_restart",
    "saved_pivot", 
    "rmemavail", 
    "time", 
    "ntasks", 
    "potential_name"]
batch_keys = [
    "run_directory",
    "account",
    "ntasks",
    "mem_per_cpu",
    "time",
    "output",
    "potential",
    "nucleus_name",
    "hbar_omega",
    "suffix",
    "Ngs",
    "ncsd_path",
    "non_IT_Nmax",
    "IT_Nmax",
    "kappa_rename"
    ]
mfdp_keys = [
    "output_file",
    "two_body_interaction",
    "two_body_file_type",
    "Z",
    "N",  
    "hbar_omega",
    "Nhw",
    "N_min",
    "N_1max",
    "N_12max",
    "parity",
    "total_2Mz",
    "iham",
    "iclmb",
    "strcm",
    "interaction_type",
    "major",
    "nshll",
    "occupation_string",
    "nsets",
    "min_nesp",
    "nskip",
    "iset1",
    "ki",
    "kf",
    "n_states",
    "gs_energy", 
    "iterations_required",
    "igt",
    "irest",
    "nhme",
    "nhw0", 
    "nhw_min",
    "nhw_restart",
    "kappa_points",
    "cmin",
    "kappa_restart",
    "kappa_vals",
    "convergence_delta",
    "three_body_interaction",
    "N_123max",
    "eff_charge_p",
    "eff_charge_n",
    "glp",
    "gln",
    "gsp",
    "gsn",
    "saved_pivot",
    "rmemavail"]

class Params(object):
    """I created this rather than just using dictionaries or something
    for parameter passing, because with dicts, I tend to lose track of which
    variables every file type needs, etc.
    
    When you create a Params object, it makes sure that all variables are
    provided, and that no extra ones are provided!"""

    def __init__(self, filetype, **kwargs):
        key_map = {
            "MFDP": mfdp_keys, 
            "MANUAL INPUT": min_keys, 
            "BATCH": batch_keys,
            "EMPTY": []}
        self.valid_keys = key_map[filetype]
        
        # ensure all kwargs are provided, nothing more
        if all(key in self.valid_keys for key in kwargs.keys()):
            if len(kwargs.keys()) == len(self.valid_keys):
                # then set self.kwarg = kwarg value
                for key in self.valid_keys:
                    setattr(self, key, kwargs[key])
            else:
                raise ValueError(
                    "Invalid number of parameters for "+filetype) 
        else:
            raise ValueError(
                "Not all parameters supplied to "+filetype+" were valid!")

    def param_dict(self):
        """returns a dict with the same info contained in the Params object"""
        pdict = {}
        for key in self.valid_keys:
            pdict[key] = getattr(self, key)
        return pdict

class MinParams(Params):
    def __init__(self, **kwargs):
        super(MinParams, self).__init__("MANUAL INPUT", **kwargs) 

class BatchParams(Params):
    def __init__(self, **kwargs):
        super(BatchParams, self).__init__("BATCH", **kwargs)

class MFDPParams(Params):
    def __init__(self, **kwargs):
        super(MFDPParams, self).__init__("MFDP", **kwargs)