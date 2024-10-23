# Instructions for WarpX on laptop

## *WARNING!*
  
**Before starting the installation of Smilei you MUST follow the instructions in `Laptop_Setup.md`**

## WarpX Documentation
https://ecp-warpx.github.io/  and https://warpx.readthedocs.io/en/latest/

## WarpX Build on Linux

### WarpX dependencies set-up
The setup of the environment to compile WarpX should be already active after following the commands in `Laptop_Setup.md`

### Compile WarpX
Follow these instructions to install Smilei on your Linux laptop. For Windows laptop, you might use these same instructions and build Smilei in your Linux platform.

Download the source code in the `$HOME`:
```bash
cd 
git clone https://github.com/ECP-WarpX/WarpX.git
```
Move to the downloaded directory:
```bash
cd WarpX
```
Configure your build:
```bash
cmake -S . -B build_omp -DWarpX_COMPUTE=OMP -DWarpX_FFT=ON -DWarpX_QED_TABLE_GEN=ON -DWarpX_DIMS="1;2;RZ;3"
```
If you need to change some configuration options (e.g. choose dimensionality, GPU support vs. CPU only, etc.), type this command and edit the options (advanced options available with 't'):
```bash
ccmake build
```
To save the changes press 'g'. Then build with the following command:
```bash
cmake --build build_omp -j 2
```

## WarpX Build on MacOS (TO UPDATE)

Firstly, prepare the terminal for the building of WarpX by:
```bash
brew update
brew tap openpmd/openpmd
```
then force the use of *clang* (Apple default compiler) with *libomp* to let the first be able to use OpenMPI commands:
```bash
export CXX=$(which clang++)
brew unlink gcc
brew link --force libomp
```
this latter process might create some error in the future, so at the end of the compiling remind to unlink *libomp* with the following commands:
```bash
brew unlink libomp
brew link gcc
```
Then, you have prepared your terminal for compiling WarpX. Clone repository and move there 
```bash
git clone https://github.com/ECP-WarpX/WarpX.git warpx
cd warpx
```
Configure build 
```bash
cmake -S . -B build
```
If you need change the configuration options (e.g. choose dimensionality - default is 3D, GPU support vs. CPU only)
```bash
ccmake build
```
Build (the *8* stands for the number of processes, use the right one for your laptop):
```bash
cmake --build build -j 8
```
then proceed with compilation.

## Run WarpX
Once you've installed WarpX, you have executables (for 1D, 2D, 3D and cylindrical geometries) ready to perform simulations which are found in `$HOME/WarpX/build_omp/bin/`. These executables need an input file `input.py` file to set up the simulation you want to perform. An input file contains numerical, physical and diagnostic parameters (refer to https://smileipic.github.io/Smilei/Use/namelist.html for a detailed description). You can find examples of input files in `PiC_Scripts` folder.

Move to the directory where the `input.py` file was created. Set the number of threads per core depending on the machine; for example, if Thread(s) per core = 2 (in the output of the commands shown at the end of the **Before starting** section of `Laptop_Setup.md`), then
```bash
export OMP_NUM_THREADS=2
```

and if you have Core(s) per socket = 4, you can run on the 4 cores like this 
```bash
mpirun -np 4 $HOME/WarpX/build_omp/bin/warpx.2d.MPI.OMP.DP.PDP.OPMD.QED input.txt warpx.numprocs = 1 4
```
note that the executable for 2D simulations is being used and that `warpx.numprocs` flag is optional.

## Analyze WarpX output
To open and analyze the binary files in output from WarpX you need to install 'openpmd' (see http://www.openpmd.org/ and https://openpmd-api.readthedocs.io/en/latest/ for documentation about it). In your Python environment do:
```bash
pip install openpmd-api
```
Now you should have the necessary software to post-process WarpX data with Python, i.e. in a Python script you can do:
```bash
import openpmd_api as io
```
