# ncsd_python

Python modules to make your life easy while running `ncsd-it.exe`! Main script is `ncsd_multi.py`.
You feed it a list of parameters and a `mfdp.dat` file, and it'll run multiple ncsd jobs.

## Getting Started

`git clone` this, or if you're on Cedar you can find a clone in `exch`. `git pull origin master` to get the latest version. 

Then you'll need to open `ncsd_multi.py` and tell it where to find the executable `ncsd` file,
as well as interaction files.


```
    manual_params = MinParams(
        # paths
        mfdp_path = "/path/to/some/template/mfdp.dat",
        interactions_directory = "/path/to/interactions",
        ncsd_path = "/path/to/ncsd-it.exe",
        two_body_interaction = "TBMEA2srg-n3lo2.0_14.20_910",
        ...
    )
```

To do multiple runs, simply specify a variable as a list, e.g. `Z = [3,4,5]` will make 3 different runs.

Make sure that your variables are well paired if more than one is changing, runs are created by list index!

If you have variables that change, but less than others, keep in mind that lists are extended by copying their last entry,
not by some other method.

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

Just Python (3.7.4 ideally, other versions may work), ncsd-it.exe, the other input files, and hopefully knowledge about what all the parameters do!

No other libraries or downloads or anything are needed.
