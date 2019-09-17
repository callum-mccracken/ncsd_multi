"""contains functions to check various sorts of data"""
import sys
from os.path import join, exists
from sub_modules.parameter_calculations import Ngs_func

def manual_input_check(params):
    """checks manual input to ensure it is at least self-consistent"""
    print("checking manual input")
    # do we have a 3-body interaction?
    three_body = (abs(params.interaction_type) == 3)
    
    # first check if paths exist
    if not exists(params.interactions_directory):
        raise IOError("Interactions directory " + \
            params.interactions_directory + " does not exist")

    f2 = join(params.interactions_directory, params.two_body_interaction)
    if not exists(f2):
        raise IOError("Two body file "+f2+" does not exist")
    if three_body:
        f3 = join(params.interactions_directory, params.three_body_interaction)
        if not exists(f3):
            raise IOError("Three body file "+f3+" does not exist")
    if not exists(params.ncsd_path):
        raise IOError("NCSD file "+params.ncsd_path+" does not exist!")

    # check that parameters make sense
    if not (params.N_12max >= params.N_1max):
        raise ValueError("N_12max must be >= N_1max")
    if three_body:
        if not (params.N_123max >= params.N_12max):
            raise ValueError("N_123max must be >= N_12max")

    # check there's at least kappa_points kappa values
    kappa_vals = list(map(float, params.kappa_vals.split()))
    if len(kappa_vals) < params.kappa_points:
        raise ValueError("You must have at least kappa_points kappa values!"+\
            " kappa_points = "+params.kappa_points)
    
    # and if kappa_points and kappa_vals disagree, make sure they know that
    if len(kappa_vals) > params.kappa_points:
        print("Did you mean to enter "+str(len(kappa_vals))+\
            " values for kappa_min, but set kappa_points to "+\
            str(params.kappa_points)+"?")
        
        user_input = ""
        while user_input not in ["Y", "N"]:
            user_input = input("Enter Y to proceed, N to cancel: ")
        if user_input == "N":
            print("Okay, exiting... Try again!")
            sys.exit(0)

    kr_values = [-1, 1, 2, 3, 4]
    if params.kappa_restart not in kr_values:
        raise ValueError("kappa_restart must be one of"+" ".join(kr_values))
    
    if params.saved_pivot not in ["F", "T"]:
        raise ValueError("saved_pivot must be either T or F")
    
    if (params.irest == 1 or params.kappa_restart != -1
       or params.nhw_restart != -1) and params.saved_pivot == "F":
        raise ValueError("why not use the saved pivot if you're restarting?")
    
    
    # if this function runs, the input passes the test

def check_mfdp_read(mfdp_params):
    """checks to see if mfdp data, read from a file, was ok"""    
    print("opening mfdp file, checking data")
   
    # 3 body interaction?
    three_body = (abs(mfdp_params.interaction_type) == 3)

    # there must be a better way than hard-coding all these indices, right?

    # parse TBME file for parameters
    directories = mfdp_params.two_body_interaction.split("/")
    tbme_filename = directories[-1] # last one's the actual file
    tbme_type = int(tbme_filename[5])
    last_chunk = tbme_filename.split(".")[-1]
    [hbar_omega_verif_0, other_stuff] = last_chunk.split("_")
    hbar_omega_verif_0 = float(hbar_omega_verif_0)
    N_1max_verif = int(other_stuff[0])
    N_12max_verif = int(other_stuff[1:])

    # parse output file name
    sections = mfdp_params.output_file.split("_")
    the_rest = sections[2]
    dot_sections = the_rest.split(".")
    hbar_omega_verif_1 = float(dot_sections[1])

    # parse 3-body
    if three_body:
        # check 3-body file?
        pass

    message = ""  # adjust error message as needed

    # check obvious things
    if mfdp_params.saved_pivot not in ["F", "T"]:
        message = "saved_pivot must be either T or F"
    if mfdp_params.two_body_file_type != tbme_type:
        message = "TBME type does not match type from TMBE filename"
    if mfdp_params.hbar_omega != hbar_omega_verif_0:
        message = "freq does not match freq from TMBE filename"
    if mfdp_params.hbar_omega != hbar_omega_verif_1:
        message = "freq does not match freq from output filename"
    if mfdp_params.N_1max != N_1max_verif:
        message = "N_1max does not match value from TBME filename"
    if mfdp_params.N_12max != N_12max_verif:
        message = "N_12max does not match value from TBME filename"
    if mfdp_params.eff_charge_p != 1.0:
        message = "effective charge of proton is 1.0, not "+str(mfdp_params.eff_charge_p)
    if mfdp_params.eff_charge_n != 0.0:
        message = "effective charge of neutron is 0.0, not "+str(mfdp_params.eff_charge_n)
    if mfdp_params.glp != 1.0:
        message = "glp is always 1.0, not "+str(mfdp_params.glp)
    if mfdp_params.gln != 0.0:
        message = "gln is always 1.0, not "+str(mfdp_params.gln)
    if mfdp_params.gsp != 5.586:
        message = "gsp is always 5.586, not "+str(mfdp_params.gsp)
    if mfdp_params.gsn != -3.826:
        message = "gsn is always -3.826, not "+str(mfdp_params.gsn)
    
    # mod 2 checks
    if ((mfdp_params.Z + mfdp_params.N) % 2) == 0:
        if mfdp_params.total_2Mz != 0:
            message = "Z + N is even, so total_2Mz must be 0, not "+str(mfdp_params.total_2Mz)
    else:
        if mfdp_params.total_2Mz != 1:
            message = "Z + N is odd, so total_2Mz must be 1, not "+str(mfdp_params.total_2Mz)

    if mfdp_params.parity != (mfdp_params.Nhw % 2):
        message = "we require parity = Nhw mod 2"
    if mfdp_params.parity != (mfdp_params.nhw0 % 2):
        message = "we require parity = nhw0 mod 2"
    if mfdp_params.parity != (mfdp_params.nhw_min % 2):
        message = "we require parity = nhw_min mod 2"

    # raise last error detected
    if message:
        raise ValueError("Bad template MFDP file: "+message)