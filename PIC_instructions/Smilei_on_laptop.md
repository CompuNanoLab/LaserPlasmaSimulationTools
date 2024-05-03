# Documentation
https://smileipic.github.io/Smilei

# Build on Linux
download the source code
```
git clone https://github.com/SmileiPIC/Smilei.git smilei
```

move to the right directory
```
cd smilei
``` 

source spack if you don't do it in your `bash.rc` 
```
source $SPACK_DIR/share/spack/setup-env.sh
```

load the smilei enviroment 
```
spack env activate -p myspacksmilei
```

set the environment variable `HDF5_ROOT_DIR` to the path where the correct installation of hdf5 is  
you can find the path in the output of the following command 
```
spack find --path hdf5+mpi ^openmpi %gcc@10.2.1
```
for example in my case
```
export HDF5_ROOT_DIR =$HOME/src/spack/opt/spack/linux-debian11-skylake/gcc-10.2.1/hdf5-1.12.2-aqc4gaolbexiqq7wvne2bhewi6fjxet3
export LD_LIBRARY_PATH=${HDF5_ROOT_DIR}/lib:${LD_LIBRARY_PATH}
```

set also this other environment variable 
```
export PYTHONEXE=python3
``` 

you can set the environment variables in your `.bashrc` file

then compile
```
make -j 2
``` 

build the python module to manage output 
```
make happi
```

in a python script you can now do
```
import happi
```

# Build on Mac

Firstly you need to install Homebrew (check Basics.md). Then you could either follow the steps on:

https://smileipic.github.io/Smilei/Use/install_macos.html#brew-install-smilei

Either installing the dependencies as shown here:
```
brew install iltommi/brews/smilei --HEAD --only-dependencies
```
Or following the commands on *Dependencies_on_laptop.md* (this second one might be preferred even though little more tedious).

Then, update the profile `~/.zprofile` (or `~/.bash_profile` in some older versions of MacOS):
```
cd
nano .zprofile
```
and add the following lines:
```
export OMPI_CXX=g++-13
export HDF5_ROOT_DIR=/opt/homebrew/opt/hdf5-mpi
export PYTHONEXE=python3
export SITEDIR=~/myenv/lib/python3.12/site-packages
```
You may need to change the `g++-13` to some other version you have on your laptop. To check the version use the `brew info gcc` command, do not forget the number of the version: by using in fact `g++` only, you will call `clang++` compiler which is provided by Apple. Such a compiler does not work with `openmpi` that is necessary for Smilei compilation instead.

Use then `git` to copy Smilei on your home:
```
git clone https://github.com/SmileiPIC/Smilei.git smilei
```
move in the folder and open the makefile. Look for `SITEDIR` and add a `?` in front of the `=`. Use then `make` to copile the source (remind to activate the python environment):
```
cd smilei
make -j 8
```
To use the post-processing tools offered by Smilei, once you have compiled the source:
```
make happi
```

# Run 
copy the executable (smilei) and an input file (input.py) in a directory (mydir) and move there 

set the number of threads per core depending on the machine 
for example, if Thread(s) per core = 2 (in the output of the `lscpu` command), then
```
export OMP_NUM_THREADS=2
```

and if you have Core(s) per socket = 4, you can run on the 4 cores like this 
```
mpirun -np 4 ./smilei input.py
```
