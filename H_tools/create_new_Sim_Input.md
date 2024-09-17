# How to create a new application with FLASH (work in progress)

This tutorial is useful after having performed at least the first compilation process shown in `FLASH_on_Galileo100.md`. 
In order to create your simulation you have to move inside `FLASH4.8` folder and from there to `source/Simulation/SimulationMain`.
Here you might want to create a new folder (e.g `YOUR_FOLDER`)for your simulation. You will need to have following files inside the folder:
```bash
Makefile
Simulation_customizeProlong.F90
Simulation_data.F90
Simulation_initBlock.F90
Simulation_init.F90
your_sim.par
species.cn4
```
The file `Simulation_initBlock.F90` will contain all the customised routines to initialise the species initial conditions and positions. 
The file `your_sim.par`, instead, will contain the specific parameters needed for the initialisation of both species and laser. 
You might want also to add a `Simulation_adjustEvolution.F90` file to make the `BDRY_VAR` changing with temperature to mimic the solid behaviour.
When `BDRY_VAR` is set to `1` the body will behave as a perfect solid, while when set to `-1` as a fluid. Thus, making it change from `1` to `-1`
at the melting temperature could mimic the solid behaviour. The files `species.cn4` are the `IONMIX4` opacities and EOS needed to solve the 
hydrodynamics problem, other formats (such as `sesame`) are accepted. 

To run the simulation you need then to change the parameters to be given to `setup` scripts with the wanted conditions. For example, a 2D cartesian 
simulations with two species (`targ` and `cham`) could be set as follows:
```bash
./setup -auto YOUR_FOLDER -2d +cartesian +pm4dev --nxb=16 --nxb=16 +hdf5typeio +parallelIO species=cham,targ +mtmmmt +laser +uhd3t +mgd mgd_meshgroups=6 -parfile=your_sim.par
```
The setup will use blocks having 16x16 points per block, with parallel HDF5 I/O, using a multi-temperature radiative hydrodynamic algorithm and considering energy deposition 
by a laser. Opacities will be computed by approximating in 6 groups.
