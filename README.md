# ncsd_multi

Python modules to make your life easy while running `ncsd-it.exe`!

Main script is `ncsd_multi.py`.
You feed it a list of parameters,
and it'll run multiple ncsd jobs for you.

## Getting Started

`git clone` this, or if you're on Cedar you can find a clone in `exch`.

To get the latest version (*note that this removes any local changes*), do:

`git fetch --all`

`git reset --hard origin/master`

Then you'll need to open `ncsd_multi.py` and enter a bunch of parameters:

- `ncsd_path = realpath("ncsd-it.exe")`
  - edit this so it's the path to your ncsd executable file
  - relative paths are okay inside the `realpath()` function
- `working_dir = realpath("")`
  - make this the path to the directory where to want to complete the ncsd runs

```    
    manual_params = ManParams(
        ...
        Z = 3,  # number of protons
        N = [5,6],  # number of neutrons
        hbar_omega = 20,  # harmonic oscillator frequency
        N_1max = 9,  # highest possible excited state of 1 nucleon
        N_12max = 10,  # highest possible state of 2 nucleons, added
        ...
    )
```
  - enter your calculation-related parameters here

- `ncsd_multi_run(man_params, run=True)`
  - change the `True` to `False` if you don't want to run all batch files

- There are other parameters which are set by default, e.g. `iclmb`
  - Those can be changed by going to the very bottom of `data_structures.py`
    and editing the inputs to `DefaultParamsObj`


### To do multiple runs, simply specify at least one variable as a list.
e.g. `Z = [3,4,5]` will make 3 different runs.

Make sure that your variables are well ordered if more than one is changing,
runs are created by list index!

If you have variables that change, but less than others,
keep in mind that lists are extended by copying their last entry.

So if you have

`Z = [1,2]`
`N = [1,2,3]`
`Nhw = 1`

you'll get 3 runs, with parameters

`Z = [1,2,2]`
`N = [1,2,3]`
`Nhw = [1,1,1]`


Note: make sure to edit the 3-body parameters if `abs(interaction_type) == 3`.

### Prerequisites

Just Python (3.7.4 ideally, other versions may work).

You'll need an executable ncsd file and interaction files too, of course.