# Instructions for PiC codes on Leonardo
Before installing PiC codes on Leonardo read `Cineca_HPC_systems_setup.md`.

## Smilei on Leonardo

### Smilei Documentation
https://smileipic.github.io/Smilei

### Smilei dependencies setup
Create a `smilei.profile` file in your `$HOME` containing the following lines (TO UPDATE):
```bash
module purge
module load python
module load profile/archive
module load nvhpc/23.1
module load zlib/1.2.13--gcc--11.3.0
module load openmpi/4.1.4--nvhpc--23.1-cuda-11.8
module load hdf5/1.12.2--openmpi--4.1.4--nvhpc--23.1
module load boost/1.80.0--openmpi--4.1.4--nvhpc--23.1

export SMILEICXX_DEPS=g++
export CXXFLAGS="-w -gpu=cc80 -acc -std=c++14  -lcurand -cudalib=curand -Minfo=accel -D__GCC_ATOMIC_TEST_AND_SET_TRUEVAL=1"
export GPU_COMPILER_FLAGS="-O3 --std c++14 -arch=sm_80 -expt-relaxed-constexpr"
export LDFLAGS="-gpu=cc80 -acc -cuda -std=c++14 -cudalib=curand -lcudart -lcurand -lacccuda"
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
make -j 16 config="gpu_nvidia"
```
If it compiles successfully, you will find the executable `smilei` in the current directory. Another executable `smilei_test` is generated to be run in test mode (e.g. use it to check that the input file is ok).

### Run Smilei
To run a Smilei simulation follow these steps:
* Create a directory `$MYDIR` in your scratch.
* Put in this directory a valid `input.py`. 
* Be sure to have the `Smilei` directory and the `smilei.profile` file in your `$HOME`, and to have successfully compiled Smilei.
* Prepare your job script `job.sh` and submit it with the command `sbatch job.sh`.
Here is an example of what `job.sh` could contain:
```bash
#!/bin/bash
#SBATCH --time=08:00:00
#SBATCH --nodes=128
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-socket=4
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-node=4
#SBATCH --gpus-per-task=1
#SBATCH --mem=494000
#SBATCH -p boost_usr_prod
#SBATCH --qos=boost_qos_bprod
#SBATCH --job-name=jobName
#SBATCH --gres=gpu:4
#SBATCH --err=smilei.err
#SBATCH --out=smilei.out
#SBATCH --account=ProjectName
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your.mail@polimi.it

cd /leonardo_scratch/large/userexternal/your_username/path/for/the/simulation

source $HOME/smileinew.profile
srun $HOME/Smilei/smilei input.py > output.txt
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
cd $HOME/
```
A message like `Installing leonardo/home/userexternal/your_username/.local/lib/python3.11/site-packages/smilei.pth` should be shown at screen. Copy the path and follow the next steps:
```
bash
cd $HOME/myenv/lib/python3.11/site-packages/
cp /leonardo/home/userexternal/your_username/.local/lib/python3.11/site-packages/smilei.pth .
```
## WarpX on Leonardo

### WarpX Documentation
https://ecp-warpx.github.io/  and https://warpx.readthedocs.io/en/latest/
Instructions to build and run WarpX on Leonardo are also available here: https://warpx.readthedocs.io/en/latest/install/hpc.html.

### WarpX dependencies setup
Create a `warpx.profile` file in your `$HOME` containing the following lines (TO UPDATE):
```bash
TO DO
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
cmake -S . -B build_gpu -DWarpX_COMPUTE=CUDA -DWarpX_QED_TABLE_GEN=ON -DWarpX_DIMS="1;2;RZ;3"
```
If you need to change some configuration options (e.g. choose dimensionality, GPU support vs. CPU only, etc.), type this command and edit the options (advanced options available with `t`):
```bash
ccmake build_omp
```
To save the changes press `c` and `g`. Then build with the following command:
```bash
cmake --build build_gpu -j 16
```
If it compiles successfully, you will find the executables in `WarpX/build_gpu/bin/`.

### Run WarpX
To run a WarpX simulation follow these steps:
* Create a directory `$MYDIR` in your scratch.
* Put in this directory a valid `input.txt`. 
* Be sure to have the `WarpX` directory and the `warpx.profile` file in your `$HOME`, and to have successfully compiled Warpx.
* Prepare your job script `job.sh` and submit it with the command `sbatch job.sh`. Here is an example of what `job.sh` could contain:
```bash
TO DO
```

### Install WarpX post-processing tools
Following the guide `Cineca_HPC_systems_setup.md`, you should already have installed the openpmd-api Python package. Otherwise you can load your Python environment and use pip to install it:
```bash
source $HOME/myenv/bin/activate
pip install openpmd-api
```
