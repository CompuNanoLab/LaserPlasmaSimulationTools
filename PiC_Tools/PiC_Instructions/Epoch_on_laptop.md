# Instructions for Epoch on laptop

## :warning: *WARNING!*
  
**Before starting the installation of Smilei you MUST follow the instructions in `Laptop_Setup.md`**

## Epoch Documentation
https://epochpic.github.io/

## Epoch Build on Linux

### Epoch dependencies set-up
The setup of the environment to compile Epoch should be already active after following the commands in `Laptop_Setup.md`

### Compile Epoch and post-processing tools
Follow these instructions to install Smilei on your Linux laptop. For Windows laptop, you might use these same instructions and build Smilei in your Linux platform.

Download the source code in the `$HOME`:
```bash
cd 
git clone --recursive https://github.com/Warwick-Plasma/epoch.git
```
Move to the downloaded directory:
```bash
cd epoch
```
and move again to choose in which dimensionality you want to compile the code (in EPOCH there are different source codes for 1D, 2D and 3D geometry). For example, to compile the 2D version of EPOCH do this:
```bash
cd epoch2d
```
Then build with the following command:
```bash
make COMPILER=gfortran
```
You can activate several compile-time options by modifying the `Makefile`. You can clean the building process with `make cleanall` (do it every time you re-compile).

It is better, then, to install the post-processing tools inside the Python virtual environment you should have created following the instructions in `Laptop_Setup.md`. So, source the environment (probably `source $HOME/myenv/bin/activate`) and then:
```bash
make sdfutils
```
Now, in a Python script or shell, you should be able to use 
```bash
import sdf 
import sdf_helper as sh
``` 
to open sdf files in output from Epoch.


## Epoch Build on MacOS (TO DO)

## Run Epoch
Once you've installed Epoch, you have an executable ready to perform simulations which is found in `$HOME/epoch2d/bin`. This executable needs an input file `input.deck` file to set up the simulation you want to perform. An input file contains numerical, physical and diagnostic parameters (refer to https://epochpic.github.io/documentation.html) for a detailed description. You can find examples of input files in `PiC_Scripts` folder.

To prepare your run, make a directory for your epoch simulation `sim_epoch`:
```bash
mkdir sim_epoch
``` 
Make a subdirectory `Data`:
```bash
cd sim_epoch 
mkdir Data
```
Copy in `sim_epoch` the epoch executable in the geometry you want to use. Copy in  `sim_epoch/Data`  an input file `input.deck`. Move to `sim_epoch` and run, for example, on 4 cores:  
```bash
echo Data | mpirun -np 4 ./epoch2d
```
