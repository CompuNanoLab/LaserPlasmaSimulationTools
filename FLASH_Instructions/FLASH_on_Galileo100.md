FLASH is a radiative hydrodynamics code which can be used to simulate the effects of the prepulse of a laser onto targets. In the following the instructions to compile the LaserSlab example will be given. First of all it is necessary to create a profile with the necessary dependencies to run the simulations. Create in the `$HOME` a `flash.profile` as follows:
```bash
module purge
module load profile/archive
module load gcc/10.2.0
module load hdf5/1.10.7--openmpi--4.1.1--gcc--10.2.0-pmi
module load parallel-netcdf/1.12.2--openmpi--4.1.1--gcc--10.2.0-pmi 
module load netlib-lapack/3.9.1--gcc--10.2.0
module load python/3.11.7--gcc--10.2.0
```
Then, it will be necessary to install `hypre`, a library used by FORTRAN to efficiently compute algebraic operations. To do so:
```bash
cd $HOME
source flash.profile
git clone https://github.com/hypre-space/hypre
```
move then inside `hypre` folder and type `./configure`. After that move into `src` and type `make -j 8` to install the libraries. 

You are ready now to compile FLASH. Move into `FLASH4.8` folder and prepare the configuration for the LaserSlab simulation, a cylindrical coordinate simulation of a hypergaussian laser interacting with a seminfinite slab (for more info see page 549 of FLASH manual) by using:
```
./setup -auto LaserSlab -2d +cylindrical +pm4dev --nxb=16 --nyb=16 +hdf5typeio +parallelIO species=cham,targ +mtmmmt +laser +uhd3t +mgd mgd_meshgroups=6 -parfile=example.par
```
Setup script will prepare a the `Makefile` of your simulation inside the `object` folder, so move inside this folder. `Makefile.h` must be modified as follows to make it working for Galileo100. The first lines shows the paths to the needed libraries to be used:
```bash
#----------------------------------------------------------------------------
# Set the HDF5/MPI library paths -- these need to be updated for your system
#----------------------------------------------------------------------------

MPI_PATH   = /g100_work/PROJECTS/spack/v0.17/prod/0.17.1/install/0.17/linux-centos8-cascadelake/gcc-10.2.0/openmpi-4.1.1-xcbaflrhirzvtiy3y5cnglgyfunavtx3/
HDF4_PATH  =
HDF5_PATH  = /g100_work/PROJECTS/spack/v0.17/prod/0.17.1/install/0.17/linux-centos8-cascadelake/gcc-10.2.0/hdf5-1.10.7-nro56d25ahurybevtgzfooxso3yhmabd
HYPRE_PATH = $HOME/hypre/src/hypre

ZLIB_PATH  = /g100_work/PROJECTS/spack/v0.17/prod/0.17.1/install/0.17/linux-centos8-cascadelake/gcc-10.2.0/zlib-1.2.11-3g2zcd6fz2nj37yjx6t4s65zk742iw63

PAPI_PATH  =
PAPI_FLAGS =

NCMPI_PATH = /g100_work/PROJECTS/spack/v0.17/prod/0.17.1/install/0.17/linux-centos8-cascadelake/gcc-10.2.0/parallel-netcdf-1.12.2-aghgranhq5kagkj5a6uhxga5pjwpvtdm
MPE_PATH   =

```
Then, it will be necessary to add the following line:
```bash
LIB_LAPACK = -llapack
```
The second part is needed to call the mpi-aware compilers, the default is `mpich`. On Galileo100 we are using `gcc`, thus modify as follows the names:
```bash
#----------------------------------------------------------------------------
# Compiler and linker commands
#
#   Use the MPICH wrappers around the compilers -- these will automatically
#   load the proper libraries and include files.  Version of MPICH prior
#   to 1.2.2 (?) do not recognize .F90 as a valid Fortran file extension.
#   You need to edit mpif90 and add .F90 to the test of filename extensions,
#   or upgrade your MPICH.
#----------------------------------------------------------------------------

FCOMP   = ${MPI_PATH}/bin/mpifort
CCOMP   = ${MPI_PATH}/bin/mpicc
CPPCOMP = ${MPI_PATH}/bin/mpicxx
LINK    = ${MPI_PATH}/bin/mpifort
```
To avoid argument mismatch you will also need to add the `-fallow-argument-mismatch` flag on the following lines:
```bash
OPENMP = -fopenmp

FFLAGS_OPT = -ggdb -c -O2 -fdefault-real-8 -fdefault-double-8 \
-Wuninitialized -fallow-argument-mismatch

#I explictly add -O0 because I found that compiling source files without
#an optimization flag generates the same object code as compiling source
#files with -O2.  The -O0 is required so that gdb no longer shows
#"<value optimized out>" for certain function arguments.

FFLAGS_DEBUG = -ggdb -c -O0 -fdefault-real-8 -fdefault-double-8 \
-pedantic -Wall -Waliasing \
-Wsurprising -Wconversion -Wunderflow \
-ffpe-trap=invalid,zero,overflow -fbounds-check \
-fimplicit-none -fstack-protector-all -fallow-argument-mismatch

FFLAGS_TEST = -ggdb -c -O0 -fdefault-real-8 -fdefault-double-8 -fallow-argument-mismatch
```
Lastly, for old compilers FLASH provided a fake `iso_c_bindings.mod` file. For new compilers you will need to comment last four lines
```bash
#ifeq ($(FLASHBINARY),true)
#iso_c_binding.mod :
#       touch $@
#endif
```
You are now able to compile by typing `make -j 8` inside object folder. From now on each Makefile will be created with the right folders for the machine, you don't need to repeat then the operation for each compilation. To run the simulation, move then to `$CINECA_SCRATCH` and
```bash
cp -rL $HOME/FLASH4.8/object/* .
```
in the desired folder. Create then a job inside the folder as follows:
```bash
#!/bin/bash
#SBATCH --time=3:00:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=48
#SBATCH --ntasks-per-socket=24
#SBATCH --cpus-per-task=1
#SBATCH --mem=375300MB
#SBATCH -p g100_usr_prod
#SBATCH --job-name=job_flash
#SBATCH --err=job.err
#SBATCH --out=job.out
#SBATCH --account=account_name
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your.mail@mail.it

cd $CINECA_SCRATCH/your/path/object

source $HOME/flash.profile
srun -m block:block ./flash4 > output.txt
```
and you can directly `sbatch job` to enter in the queue to run the simulation.
