"""
the module that calls everything once we have the input. This just makes the 
ncsd_multi.py file look cleaner.


"""
# built-in modules
from os import system, chdir, mkdir
from os.path import realpath, join, exists, abspath
from shutil import rmtree, copyfile

# our modules
from .data_structures import ManParams
from .parameter_calculations import calc_params, nucleus
from .data_checker import manual_input_check
from .file_manager import MFDP, Batch, Defaults


def prepare_input(m_params):  # m_params for manual params
    print("preparing input to be written to files")
    m_dict = m_params.param_dict()
    # make one set of inputs for each run

    # make all parameters into lists
    for key, value in m_dict.items():
        if type(value) != list:
            m_dict[key] = [value]


    # now length of longest list = number of unique runs
    num_runs = len(max(list(m_dict.values()), key=len))

    """
        Now for all other parameters make a list of length num_runs with duplicates
        of the last element if there aren't enough.

        For example, if num_runs is 4 and I've specified some parameter as...
        1 --> [1,1,1,1]
        [1,2] --> [1,2,2,2]

        This may be counterintuitive if you wanted [1,2] --> [1,1,2,2]
    """

    for key, value in m_dict.items():
        if len(value) != num_runs:  # it's also guaranteed < num_runs
            # append the last element until it's the right length
            for i in range(len(value), num_runs):
                m_dict[key].append(value[-1])

    # now make one dict for each mfdp file:
    dict_list = []  
    for i in range(num_runs):
        new_dict = {}
        for key, value in m_dict.items():
            new_dict[key] = value[i]
        dict_list.append(new_dict)
    return dict_list

def create_dirs(default_data, dict_list, paths):
    print("creating directories to store run files")    
    # the creation of this function was mostly to get intellisense to chill
    def populate_dir(default_data, man_params, paths):
        """
            Each folder will need:
            - mfdp.dat --> we'll create this from defaults + manual input
            - ncsd-it.exe --> just copy it
            - batch_ncsd --> we'll create this too
        """

        chdir(realpath(join(__file__, "..", "..")))
        int_dir, ncsd_path = paths

        # create master directory to hold runs
        master_folder = "ncsd_runs"
        if not exists(master_folder):
            print("creating directory "+realpath(master_folder))
            mkdir(master_folder)

        # make a directory for run
        run_name = nucleus(man_params.Z, man_params.N)
        dir_name = realpath(join(master_folder, run_name)) 
        # ensure we don't overwrite
        if exists(dir_name):
            new_name = input("Run '"+run_name+"' already exists. \n"\
                "Enter new name, or enter empty string to overwrite: ")
            if new_name:
                dir_name = realpath(join(master_folder, new_name))
                # TODO: do we need this: default_data.output_file = new_name
            else:
                #remove it and start from scratch    
                rmtree(dir_name)
        print("making run directory "+dir_name)
        mkdir(dir_name)
        
        # now actually calculate the parameters to write out
        [mfdp_params, batch_params] = calc_params(
            dir_name, paths, man_params, default_data.params)

        # also be sure that all the batch files actually know where their exe is
        batch_params.ncsd_path = realpath(join(dir_name, "ncsd-it.exe"))
        
        print("writing files")
        # copy ncsd-it.exe
        copyfile(ncsd_path, batch_params.ncsd_path)
        
        # write mfdp.dat file
        mfdp_path = realpath(join(dir_name, "mfdp.dat"))
        MFDP(filename=mfdp_path, params=mfdp_params).write()
        
        # write batch file
        batch_path = realpath(join(dir_name, "batch_ncsd"))
        Batch(filename=batch_path, params=batch_params).write()

        # then tell the program where it is so we can run it later
        return batch_path

    # for each set of inputs
    batch_paths = []
    for man_params_dict in dict_list:
        man_params = ManParams(**man_params_dict)
        batch_paths.append(populate_dir(default_data, man_params, paths))
    # return list of paths to be run
    return batch_paths

def ncsd_multi_run(man_params, paths, run=True):
    # check manual input
    print("checking manual input")
    manual_input_check(man_params, paths)
    
    
    # if reading data from mfdp template (deprecated)
    read_from_mfdp = False
    if read_from_mfdp:
        # returns data from mfdp file
        default_data = MFDP(filename=man_params.mfdp_path)
    else:
        # get data from defualts object
        default_data = Defaults()

    # list of dicts which contain parameters for each run
    list_of_dicts = prepare_input(man_params)
    # creates directories with runnable batch files
    batch_paths = create_dirs(default_data, list_of_dicts, paths)

    # run all batch paths if wanted
    if run:
        print("running all batch files")
        for batch_path in batch_paths:
            system("sbatch "+batch_path)
    
    print("done!")
