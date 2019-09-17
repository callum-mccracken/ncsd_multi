"""overview: facilitates running ncsd-it.exe with many nuclei
- takes sets of inputs for ncsd-it.exe runs
- then, for each run:
    - makes a folder so each run's output is contained, copies exe file
    - makes a bunch of mfdp.dat files to complete each run
    - runs each process with sbatch at the end
"""
from os.path import join, realpath, split
from os import environ, system
import sys
from sub_modules.data_structures import MinParams
from sub_modules.ncsd_multi_run import ncsd_multi_run

""" If debugging comment this out!
It suppresses tracebacks so error messages look cleaner,
but if you're debugging you want the full mess.
"""
sys.tracebacklimit = 0

# deal with environment variables and paths
try: # make INT_DIR environment variable if it doesn't exist already
    int_dir = environ["INT_DIR"]
except KeyError:
    environ["INT_DIR"] = input(
        "Enter the (full path) directory where your interactions are stored: ")
    system("echo 'export INT_DIR=\""+environ["INT_DIR"]+"\"\n' >> ~/.bash_profile")
    system(". ~/.bash_profile")
    int_dir = environ["INT_DIR"]
ncsd_python_dir = split(realpath(__file__))[0]  # this file's directory
template_path = join(ncsd_python_dir, "templates") # template and exe are here
mfdp_path = join(template_path, "mfdp_template.dat")
exe_path = join(template_path, "ncsd-it.exe")


### PARAMETERS -- specify all as single parameter or list []
# "min" since this is a minimal set needed to describe the input
min_params = MinParams(
    # paths
    mfdp_path = mfdp_path,  # template
    interactions_directory = int_dir,  # your interactions dir
    ncsd_path = exe_path,  # exe file
    two_body_interaction = "TBMEA2srg-n3lo2.0_14.20_910",  # name of 2-body interaction
    # nucleus details:
    Z = 3,  # number of protons
    N = [5,6],  # number of neutrons
    hbar_omega = 20,  # harmonic oscillator frequency
    N_1max = 9,  # highest possible excited state of 1 nucleon
    N_12max = 10,  # highest possible state of 2 nucleons, added
    # if 3-body, change these, otherwise just leave them be:
    N_123max = 11, # highest possible state of 3 nucleons, added
    three_body_interaction = "v3trans_J3T3.int_3NFlocnonloc-srg2.0_from24_220_11109.20_comp",  # name of 3-body interaction
    # computation-related parameters:
    Nmax_min = 0,  # Nmax_min and Nmax_max control how long the program runs
    Nmax_max = 8,  # i.e. 0 - 8 will give you eigenvectors for Nmax = 0,2,...,8
    Nmax_IT = 12,  # Nmax for Importance Truncation
    interaction_type = -3,  # make sure abs(interaction_type)==3 for 3-body
    n_states = 10,  # number of final states (= number of energy values)
    iterations_required = 200,  # number of iterations required in Lanczos step
    irest = 0,  # restart? 1 = yes, 0 = no
    nhw_restart = -1,  # not sure what this one does
    kappa_points = 4,  # number of kappa values
    # make sure you keep this next one written as a string!
    kappa_vals = "2.0 3.0 5.0 10.0",  # values for kappa, in increasing order
    kappa_restart = -1,  # -1 for false, else some value between 1 and 4
    saved_pivot = "F",  # "T" or "F", whether or not to use the saved pivot
    # batch file parameters:
    rmemavail = 16.0, # memory per core, in GB
    time = "0-08:00",  # DD-HH:MM, time allocated for calculation
    ntasks = 200,  # number of MPI tasks
    potential_name = "NNn3lo_3NlnlcD0.7cE-0.06-srg2.0" 
    # name of potential (above) is for output file naming purposes only
)

ncsd_multi_run(min_params)
