# Instructions for PiC codes on Galileo100
Before installing PiC codes on Galileo100 read `Cineca_HPC_systems_setup.md`.

## Smilei on Galileo100

### Smilei Documentation
https://smileipic.github.io/Smilei

### Smilei dependencies setup
Create a `smilei.profile` file in your `$HOME` containing the following lines (TO UPDATE):
```bash
module purge
module load profile/global
module load anaconda3/2020.07--gcc--8.3.1
module load intel/oneapi-2021--binary
module load intelmpi/oneapi-2021--binary
module load libszip/2.1.1--gcc--10.2.0
module load zlib/1.2.11--gcc--10.2.0
module load hdf5/1.10.7--intelmpi--oneapi-2021--binary
module load boost/1.76.0--intelmpi--oneapi-2021--binary
export SMILEICXX=mpiicpc
export HDF5_ROOT=/cineca/prod/opt/libraries/hdf5/1.10.7/intelmpi--oneapi-2021--binary
export BOOST_ROOT=/cineca/prod/opt/libraries/boost/1.76.0/intelmpi--oneapi-2021--binary/
export CXXFLAGS="-xCOMMON-AVX512 -ip -inline-factor=1000 -D__INTEL_CASCADELAKE_6248 -qopt-zmm-usage=high -fno-alias"
```
and source it:
```bash
source $HOME/smilei.profile
```

### Build Smilei 
Download the source code in your `$HOME`:
```bash
git clone https://github.com/SmileiPIC/Smilei.git
```
Move inside the directory:
```bash
cd Smilei
``` 
and compile:
```bash
make -j 16 config=omptasks
```
If it compiles successfully, you will find the executable `smilei` in the current directory. Another executable `smilei_test` is generated to be run in test mode (e.g. use it to check that the input file is ok).

### Run Smilei
To run a Smilei simulation follow these steps:
* Create a directory `$MYDIR` in your scratch.
* Put in this directory a valid `input.py`. 
* Be sure to have the `Smilei` directory and the `smilei.profile` file in your `$HOME`, and to have successfully compiled Smilei.
* Prepare your job script `job.sh` and submit it with the command `sbatch job.sh`.
Here is an example of what `job.sh` could contain if you want to run on the serial partition on 4 cores with 4 MPI tasks and 1 OMP thread per task:
```bash
#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=31200MB 
#SBATCH -p g100_all_serial
#SBATCH --job-name=job_smilei
#SBATCH --err=smilei.err
#SBATCH --out=smilei.out
#SBATCH --account=<project_name>
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mymail@mymail.com
cd $CINECA_SCRATCH/$MYDIR 
source $HOME/smilei.profile
export OMP_SCHEDULE=dynamic
export OMP_NUM_THREADS=1
srun --cpus-per-task $OMP_NUM_THREADS --cpu-bind=cores -m block:block $HOME/Smilei/smilei input.py > output.txt
```
Here is an example of what `job.sh` could contain if you want to run on the serial partition on 4 cores with 1 MPI task and 4 OMP threads per core:  
```bash
#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=31200MB 
#SBATCH -p g100_all_serial
#SBATCH --job-name=job_smilei
#SBATCH --err=smilei.err
#SBATCH --out=smilei.out
#SBATCH --account=<project_name>
#SBATCH --qos=noQOS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mymail@mymail.com
cd $CINECA_SCRATCH/$MYDIR 
source $HOME/smilei.profile
export OMP_SCHEDULE=dynamic
export OMP_NUM_THREADS=4
srun --cpus-per-task $OMP_NUM_THREADS --cpu-bind=cores -m block:block $HOME/Smilei/smilei input.py > output.txt
```
Here are some tips for parallelization from the Smilei documentation: https://smileipic.github.io/Smilei/Understand/parallelization.html#practical-setup

:warning: Warning: performances are extremely sensitive to the number of patches you use (which has to be a power of 2 in each direction) and you may have to redefine the number of cells in your simulation to optimize the number of patches you can use (often, the more the better).

### Install Smilei post-processing tools
Load `smilei.profile` and your Python environment, then move to the Smilei source directory:
```bash
source $HOME/smilei.profile
source $HOME/myenv/bin/activate
cd $HOME/Smilei
```
Build the post-processing Python package `happi`:
```bash
make happi
```
A message like this should appear:
```bash
Installing /g100/home/userexternal/<username>/.local/lib/python<...>/site-packages/smilei.pth
```
Copy the smilei.pth path in the correct directory of your Python environment:
```bash
cp /g100/home/userexternal/<username>/.local/lib/python<...>/site-packages/smilei.pth $HOME/myenv/lib/python<...>/site-packages
```
Now you should be able to `import happi` in a Python shell or script and you can use your plot files to post-process your smilei data as you would do on your computer (provided that you source your Python environment first).

## WarpX on Galileo100

### WarpX Documentation
https://ecp-warpx.github.io/  and https://warpx.readthedocs.io/en/latest/

### WarpX dependencies setup
Create a `warpx.profile` file in your `$HOME` containing the following lines (TO UPDATE):
```bash
module purge
module load gcc/10.2.0
module load cmake/3.21.4
module load profile/advanced
module load openmpi/4.1.1--gcc--10.2.0-cuda--11.1.0
module load zlib/1.2.11--gcc--10.2.0
module load adios/1.13.1--openmpi--4.1.1--gcc--10.2.0-cuda--11.1.0
module load boost/1.74.0--openmpi--4.1.1--gcc--10.2.0-cuda--11.1.0
```
and source it:
```bash
source $HOME/warpx.profile
```
### Build WarpX
Download the source code in your `$HOME`:
```bash
git clone https://github.com/ECP-WarpX/WarpX.git
```
Move inside the directory:
```bash
cd WarpX
``` 
Configure your build:
```bash
cmake -S . -B build_omp -DWarpX_COMPUTE=OMP -DWarpX_QED_TABLE_GEN=ON -DWarpX_DIMS="1;2;RZ;3"
```
If you need to change some configuration options (e.g. choose dimensionality, GPU support vs. CPU only, etc.), type this command and edit the options (advanced options available with `t`):
```bash
ccmake build_omp
```
To save the changes press `c` and `g`. Then build with the following command:
```bash
cmake --build build_omp -j 16
```
If it compiles successfully, you will find the executables in `WarpX/build_omp/bin/`. If you have problems with the pre-installed adios, you may want to try and install it from source by following the instructions here: https://adios2.readthedocs.io/en/latest/setting_up/setting_up.html#install-from-source. 
Create a  `warpx.profile` file working with ADIOS2 (TO UPDATE):
```bash
module purge
module load profile/global
module load cmake/3.21.4
module load gcc/10.2.0
module load openmpi/4.1.1--gcc--10.2.0-cuda-11.5.0
module load boost/1.77.0--openmpi--4.1.1--gcc--10.2.0
module load zlib/1.2.11--gcc--10.2.0
export ADIOS2_DIR=$HOME/ADIOS2/install/
```
Source it and install ADIOS2 in this way:
```bash
source ~/warpx.profile
git clone https://github.com/ornladios/ADIOS2.git ADIOS2
cd ADIOS2
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$HOME/ADIOS2/install ..
make -j 32
make install
```
Then follow the instructions above to install WarpX.

### Run WarpX
To run a WarpX simulation follow these steps:
* Create a directory `$MYDIR` in your scratch.
* Put in this directory a valid `input.txt`. 
* Be sure to have the `WarpX` directory and the `warpx.profile` file in your `$HOME`, and to have successfully compiled Warpx.
* Prepare your job script `job.sh` and submit it with the command `sbatch job.sh`. Here is an example of what `job.sh` could contain:
```bash
#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=31200MB 
#SBATCH -p g100_all_serial
#SBATCH --job-name=job_warpx
#SBATCH --err=warpx.err
#SBATCH --out=warpx.out
#SBATCH --account=<project_name>
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mymail@mymail.com
export MYDIR=path/to/your/simulation/directory
cd $CINECA_SCRATCH/$MYDIR
source $HOME/warpx.profile
export OMP_SCHEDULE=dynamic
export OMP_NUM_THREADS=1
srun --cpu-bind=cores $HOME/WarpX/build/bin/warpx.2d.MPI.OMP.DP.PDP.OPMD.EB.QED.GENQEDTABLES input.txt > output.txt
```

### Install WarpX post-processing tools
Following the guide `Cineca_HPC_systems_setup.md`, you should already have installed the openpmd-api Python package. Otherwise you can load your Python environment and use pip to install it:
```bash
source $HOME/myenv/bin/activate
pip install openpmd-api
```

## EPOCH on Galileo100

### Epoch Documentation
https://epochpic.github.io/

### Epoch dependencies setup
Create an `epoch.profile` file in your `$HOME` containing the following lines (TO UPDATE):
```bash
module purge
module load intel/oneapi-2022--binary
module load intelmpi/oneapi-2022--binary
module load python/3.8.12--intel--2021.4.0
```
and source it:
```bash
source $HOME/epoch.profile
```

### Build Epoch
Download the source code in your `$HOME`:
```bash
git clone --recursive https://github.com/Warwick-Plasma/epoch.git
```
Move inside the target directory, for example:
```bash
cd epoch/epoch2d
```
and compile:
```bash
make -j8 COMPILER=intel
```
If it compiles successfully, you will find the executable in `epoch/epoch2d/bin`.

### Run Epoch
To run an Epoch simulation follow these steps:
* Create a directory `$MYDIR` in your scratch.
* In this directory, create a `Data` sub-directory. 
* Put in the `Data` directory a valid `input.deck`. 
* Be sure to have the `Epoch` directory and the `epoch.profile` file in your `$HOME`, and to have successfully compiled Epoch in the geometry you need.
* Prepare your job script `job.sh` and submit it with the command `sbatch job.sh`. Here is an example of what `job.sh` could contain:
```bash
#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=31200MB 
#SBATCH -p g100_all_serial
#SBATCH --job-name=job_epoch
#SBATCH --err=epoch.err
#SBATCH --out=epoch.out
#SBATCH --account=<project_name>
#SBATCH --qos=noQOS
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mymail@mymail.com
cd $CINECA_SCRATCH/$MYDIR
source $HOME/epoch.profile
echo Data | srun $HOME/epoch/epoch2d/bin/epoch2d > output.txt
```

### Install Epoch post-processing tools (TO UPDATE)
Load `epoch.profile` and your Python environment, then move to the Epoch source directory:
```bash
source $HOME/epoch.profile
source $HOME/myenv/bin/activate
cd $HOME/epoch
```
Build the post-processing package:
```bash
make sdfutils
```
A message similar to this should appear:
```bash
writing list of installed files to 'pybuild/files.txt'
```
Now copy all the files listed in `/epoch/SDF/utilities/pybuild/files.txt` in the correct directory of your python environment `$HOME/myenv/lib/python3.8/site-packages/`:
```bash
export MYDIR=$HOME/myenv/lib/python3.8/site-packages/
cp /g100/home/userexternal/aforment/.local/lib/python3.8/site-packages/sdf_legacy.py $MYDIR
cp -r /g100/home/userexternal/aforment/.local/lib/python3.8/site-packages/sdf_helper $MYDIR/sdf_helper
cp /g100/home/userexternal/aforment/.local/lib/python3.8/site-packages/__pycache__/sdf_legacy.cpython-38.pyc $MYDIR/__pycache__
cp /g100/home/userexternal/aforment/.local/lib/python3.8/site-packages/sdf.cpython-38-x86_64-linux-gnu.so $MYDIR
cp /g100/home/userexternal/aforment/.local/lib/python3.8/site-packages/sdf-1.0-py3.8.egg-info $MYDIR
```
You can check that you have installed sdf and sdf_helper by verifying that these commands don't give errors:
```bash
source $HOME/myenv/bin/activate
ipython3
import sdf
import sdf_helper
``` 
Now you can use the Python scripts to post-process your epoch data as you would do on your computer (provided that you source your Python environment).
