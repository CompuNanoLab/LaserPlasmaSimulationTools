# WARNING!

**Before starting the installation of Smilei you must follow the instructions in `Basics.md`**

# Documentation
https://smileipic.github.io/Smilei

# Build on Linux

## Smilei set-up
The setup of the environment to compile Smilei should be already active after following the commands in `Basics.md`

## Compile Smilei and post-processing tools
Follow the following instructions to install Smilei on your Linux laptop. For Windows laptop you might use these same instructions building Smilei in your Linux platform.

Download the source code to the path of your choice:
```bash
cd /path/of/your/choice/
git clone https://github.com/SmileiPIC/Smilei.git smilei
```
Move to the downloaded directory:
```bash
cd smilei
```
then compile:
```bash
make -j 2
```
It is better, then, to install the post-processing tools inside the Python virtual environment you should have created following the instructions in `Basics.md`. So, source the environment (probably `source ~/myenv/bin/activate` or `source /home/your_username/myenv/bin/activate` if using Windows) and then:
```bash
make happi
```

# Build on MacOS

Follow the following instructions to install Smilei on you Mac-OS laptop

## Smilei set-up

Then, update the profile `~/.zprofile` (or `~/.bash_profile` in some older versions of MacOS):
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
You may need to change the `g++-13` to some other version you have on your laptop. To check the version use the `brew info gcc` command, do not forget the number of the version: by using in fact `g++` only, you will call `clang++` compiler which is provided by Apple. Such a compiler does not work with `openmpi` that is necessary for Smilei compilation instead. After doing so, close the terminal and open a new one to set the new environment.

## Compile Smilei and post-processing tools

Use then `git` to copy Smilei on your home:
```bash
git clone https://github.com/SmileiPIC/Smilei.git smilei
```
Move in the folder and open the makefile. Look for `SITEDIR` and add a `?` in front of the `=`. Use then `make` to copile the source (remind to activate the python environment):
```bash
cd smilei
make -j 4
```
To use the post-processing tools offered by Smilei, once you have compiled the source:
```bash
make happi
```

# Run 
Copy the executable (smilei) and an input file (input.py) in a directory (mydir) and move there. Set the number of threads per core depending on the machine; for example, if Thread(s) per core = 2 (in the output of the commands shown at the end of `Basics.md`), then
```bash
export OMP_NUM_THREADS=2
```

and if you have Core(s) per socket = 4, you can run on the 4 cores like this 
```bash
mpirun -np 4 ./smilei input.py
```
