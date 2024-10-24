# Cineca High-Performance Computing systems

High-Performance Computing (HPC) systems available at Cineca (e.g. Galileo100 and Leonardo) are Linux-based machines that you can use to perform PiC simulations strongly exploiting parallelization on several CPUs or GPUs. These clusters should be used for those problems for which the computational resources of your laptop are no more enough. Below you can find essential notes on the use of these machines, but please refer to the following links for detailed and updated instructions.
* HPC user guide: https://wiki.u-gov.it/confluence/display/SCAIUS/HPC+User+Guide
* Galileo100: https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.3%3A+GALILEO100+UserGuide
* Leonardo: https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2%3A+LEONARDO+UserGuide

## Access
Create a new user here https://userdb.hpc.cineca.it/ and ask to be added to some project on an HPC machine. You can also apply for your project, called ISCRA, to get computational resources and a budget to use on these machines.

Follow the guidelines here https://wiki.u-gov.it/confluence/display/SCAIUS/How+to+connect+via+2FA to enable the double authentication, now necessary to access the machines. Once you are authenticated you can connect to the machine of your choice with these commands:

```bash
ssh <username>@login.g100.cineca.it
ssh <username>@login.leonardo.cineca.it
```

You can also create aliases in your `~/.bashrc` on your laptop to connect more easily, for example: 
```bash
alias galileo100='ssh -X <username>@login.g100.cineca.it'
alias leonardo='ssh -X <username>@login.leonardo.cineca.it'
```
then you can connect to Galileo100 by just typing `galileo100` on your terminal 

## Filesystem structure
These are the main directories that you will use on a Cineca machine:

### `$HOME`
* It's where you land when you log in.
* Permanent: files won't be removed. 
* Use this space to store your sources and binaries and other lightweight material.
* Compile your codes here, but do not run simulations here (unless extremely tiny, e.g. just to check that a binary works with a given input).
* 50 GB quota
* It's backed up. 
* User-specific and private.

### `$CINECA_SCRATCH`
* Move there by `cd $CINECA_SCRATCH`.
* User-specific.
* Private, but you can change the permissions of this directory (at your own risk) if you want to easily exchange files with another user by being able to read and browse their scratch. By default the permissions of your directory in the scratch should be `drwx------` (this is the output of  `ls -ld`). You can change this to `drwxr-xr-x`  with `chmod`:
`chmod 755 <your_directory>`: now everybody should be able to read and browse `<your_directory>`.
* Temporary: there is a periodic (daily) cleaning procedure. Files that have remained untouched for more than 40 days are removed and a file in your home is generated listing all the deleted files on a given day (if any). To avoid losing your files unintentionally, you can touch all files and subdirectories with this command: `find . -exec touch {} \;` (this however is frowned upon!)
* No disk quota but a temporary quota of 20 TB could be imposed if the cluster reaches high levels of occupancy. 

### `$WORK`
* Project-specific, so you share this with your colleagues, talk to them to decide how to use it. 
* Collaborative space.
* 1 TB quota

More info on the filesystems of Cineca machines can be found here: https://wiki.u-gov.it/confluence/display/SCAIUS/UG2.5%3A+Data+storage+and+FileSystems

## Useful commands
To get some stats on your disk storage type:
```bash
cindata
```
or, in the folder of your interest, use: 
```bash
du -hc
```
To get stats on your budget situation use:
```bash
saldo -b
```
for the global use of the project budget, or use:
```bash
saldo -r
```
For the details on how you are using the budget.

## Prepare your environment
On HPC machines, you can usually set your environment appropriately by loading the software that you need via the module command: 
```text
Command                Action
---------------------------------------------------------------------------------------------- 
module avail .................. show the available modules on the machine 
module load <appl> ............ load the module <appl> in the current shell session, preparing the environment for the application. 
module load autoload <appl> ... load the module <appl> and all dependencies in the current shell session
module help <appl> ............ show specific information and basic help on the application 
module list ................... show the modules currently loaded on the shell session 
module purge .................. unload all the loaded modules 
module unload <appl>........... unload a  specific module
modmap -m <appl>................find available <appl> 
```

If you need some software that is not available via the module command, you should try installing it from source or with spack (https://spack.readthedocs.io/en/latest/), which is installed at Cineca and you can use it after loading it: `module load spack`.

## File transfer
To transfer files from a supercomputer to your local computer or vice versa you can use `scp` or `rsync`. To copy from a remote supercomputer to your local laptop type this command on your laptop terminal: 
```bash
scp <username>@login.g100.cineca.it:<path_2_file_u_want_2_download> <path_to_local_directory>
```
or
```bash
rsync --update --progress <username>@login.g100.cineca.it:<path_2_file_u_want_2_download>  <path_to_local_directory>
```
To copy from your local laptop to a remote supercomputer, type this command in your laptop:
```bash
scp <path_2_file_u_want_2_upload> <username>@login.g100.cineca.it:<your_target_directory> 
```
or
```bash
rsync --update --progress <path_2_file_u_want_2_upload> <username>@login.g100.cineca.it:<your_target_directory>
```
To download large amounts of data you can use an automatic script based on rsync that automatically restarts when the transfer is interrupted:
```bash
#!/bin/bash
name=folder
source=<your_username>@login.g100.cineca.it:/g100_scratch/userexternal/<your_username>/${name}
echo ${source}
dest=${name}
while [ 1 ]
do
    rsync -vv --partial --progress --inplace --append --compress --recursive $source $dest
    if [ "$?" = "0" ] ; then
        echo "rsync completed normally"
        exit
    else
        echo "Rsync failure. Backing off and retrying..."
        sleep 180
    fi
done
```

## Run jobs
To run your simulations (or also Python scripts if needed) you have to submit jobs to the scheduler, which is SLURM (https://slurm.schedmd.com/documentation.html) on Cineca systems. The scheduler will put your job in a queue, assign the computational resources required, launch it, stop it when it reaches the wall time, etc.
You can use both batch jobs (recommended) or interactive jobs running on an open terminal on the machine. 

### Batch jobs 
To submit a job from batch, you need to create a script `job.sh` like the following one:
```bash
#!/bin/bash 

# slurm directives
#SBATCH --time=04:00:00 # walltime 
#SBATCH --nodes=1 # number of nodes 
#SBATCH --ntasks-per-node=4 # number of cores
#SBATCH --cpus-per-task=1 # number of mpi tasks/core
#SBATCH --mem=31200MB # memory/core
#SBATCH -p g100_all_serial # partition
#SBATCH --qos=noQOS # quality of service
#SBATCH --job-name=myname 
#SBATCH --err=myjob.err # standard error
#SBATCH --out=myjob.out # standard output
#SBATCH --account=<project_name> # account / budget
#SBATCH --mail-type=ALL # type of alerts
#SBATCH --mail-user=mymail@mymail.com # email address

# move to the directory where you want to run the code
cd /g100_scratch/userexternal/<path_details>/epoch

# source the required software, e.g. for epoch 
source epoch.profile

# run the code e.g. with srun 
echo Data | srun ./epoch2d > output.txt
```
Then, to submit your job you type the following command in the folder containing this script: 
```bash
sbatch job.sh
``` 
To check the status of the submitted job:
```bash
squeue -u <username>
```
You will see some stats of your job: the ID assigned by the scheduler, the status, the running time, etc. For additional stats on your job use this command:
```bash
scontrol show job <job_id>
```
To hold your job in queue use:
```bash
scontrol hold <jobid>
```
To release it use:
```bash
scontrol release <jobid>
```
If you want to cancel your job:
```bash
scancel <jobid>
```
To get information on the job submitted during the current day type:
```bash
sacct
```

### Interactive jobs
You can also ask for computational resources interactively: this means that you will be able to type in commands directly on the open terminal on the machine. For example, you can launch an interactive job with this command:
```bash
srun -n1 --time=04:00:00 -A <project_name> -p g100_all_serial --ntasks-per-node=1 --cpus-per-task=1 --pty /bin/bash
```
Please be aware that when you close your terminal session, the allocation will end. 

## Python environment
To use Python on HPC machines the best option is to create your own Python environment in your $HOME:
```bash
module load python
python3 -m venv myenv
source $HOME/myenv/bin/activate
```
Then, check that you can use your Python environment with:
```bash
which python
which pip
```
You can easily install the required software with `pip`:
```bash
pip install numpy 
pip install scipy 
pip install ipython 
pip install matplotlib 
pip install openpmd-api
``` 
