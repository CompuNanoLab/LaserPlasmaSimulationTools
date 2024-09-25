# Instructions for Smilei on laptop

## *WARNING!*
  
**Before starting the installation of Smilei you MUST follow the instructions in `Laptop_Setup.md`**

## Smilei Documentation
https://smileipic.github.io/Smilei

## Smilei Build on Linux

### Smilei dependencies set-up
The setup of the environment to compile Smilei should be already active after following the commands in `Laptop_Setup.md`

### Compile Smilei and post-processing tools
Follow these instructions to install Smilei on your Linux laptop. For Windows laptop you might use these same instructions and build Smilei in your Linux platform.

Download the source code in the `$HOME`:
```bash
cd 
git clone https://github.com/SmileiPIC/Smilei.git
```
Move to the downloaded directory:
```bash
cd smilei
```
then compile:
```bash
make -j 2
```
It is better, then, to install the post-processing tools inside the Python virtual environment you should have created following the instructions in `Laptop_Setup.md`. So, source the environment (probably `source ~/myenv/bin/activate` or `source /home/your_username/myenv/bin/activate` if using Windows) and then:
```bash
make happi
```

## Smilei Build on MacOS

Follow these instructions to install Smilei on you MacOS laptop

### Smilei dependencies set-up

Update the profile `~/.zprofile` (or `~/.bash_profile` in some older versions of MacOS) using `nano`:
```bash
cd
nano .zprofile
```
and add the following lines:
```bash
export OMPI_CXX=g++-13
export HDF5_ROOT_DIR=/opt/homebrew/opt/hdf5-mpi
export PYTHONEXE=python3
export SITEDIR=~/myenv/lib/python3.12/site-packages
```
You may need to change the `g++-13` to some other version you have on your laptop. To check the version use the `brew info gcc` command, do not forget the number of the version: in fact, by using `g++` only, you will call `clang++` compiler provided by Apple. Such a compiler does not work with `openmpi` that is necessary for Smilei compilation instead. After doing so, close the terminal and open a new one to set the new environment.

### Compile Smilei and post-processing tools

Use `git` to copy Smilei on your home:
```bash
git clone https://github.com/SmileiPIC/Smilei.git
```
Move in the folder and open the makefile (possibly with your graphic interface, so that you can use `crtl + F` to find what you're looking for). Look for `SITEDIR` and add a `?` in front of the `=`. Use then `make` to copile the source (remind to activate the python environment):
```bash
cd smilei
make -j 4
```
To use the post-processing tools offered by Smilei, once you have compiled the source:
```bash
make happi
```

## Run Smilei
Once you've installed Smilei, you have an executable ready to perform simulations which is found in `$HOME/Smilei/smilei`. This executable needs an input file `input.py` file to set up the simulation you want to perform. An input file contains numerical, physical and diagnostic parameters (refer to https://smileipic.github.io/Smilei/Use/namelist.html for a detailed description). You can find examples of input files in `PiC_Scripts` folder.

Move in the directory where the `input.py` file was created. Set the number of threads per core depending on the machine; for example, if Thread(s) per core = 2 (in the output of the commands shown at the end of the **Before starting** section of `Laptop_Setup.md`), then
```bash
export OMP_NUM_THREADS=2
```

and if you have Core(s) per socket = 4, you can run on the 4 cores like this 
```bash
mpirun -np 4 ./smilei input.py
```
