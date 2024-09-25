# Laptop
## General dependencies
This file contains the instructions to install general dependencies in your laptop based on your Operative System.

### Windows
In order to use most of the Laser-Plasma simulation tools in Windows, you must set up a running Linux platform:

- Go to Start. Search for "Turn Windows features on or off."
- Check the option Windows Subsystem for Linux:
  
  <img src="/PiC_Tools/Images/322772146-75fe59a8-35c6-47c9-9b3e-fef7ff2c0fad.png" width="400" />
  
- Open Command Prompt as an administrator:
  
  <img src="/PiC_Tools/Images/322772777-96052034-10c0-417a-90dc-71180df4704d.png" width="400" />
  
- Run the command below to install the *Distro* (e.g. Ubuntu, Debian, ...; suggested ones: Debian or Ubuntu) of your choice:
  ```
  wsl --install -d <Distro>
  ```
- Launch the *Distro* by searching from the start menu and insert a username and password. Remember that when you launch the virtual machine you are opening a terminal in the ```$HOME``` of your Linux platform.
  
  <img src="/PiC_Tools/Images/327967584-fb762f06-3d6b-4ddc-b090-e2569d73d3fa.png" width="400" />

You can access the files of your virtual machine by opening the Windows File Explorer and looking for the Linux folder. Inside the folder with the name of your Distro you can find your ```home``` directory.

<img src="/PiC_Tools/Images/327968742-3278d5b3-cbc6-43a3-959e-78b11d40ac9a.png" width="600" />

Follow then the instructions for the *Distro* that you chose.

### Debian-based (Ubuntu) OS:
To install the dependencies on your Debian-based laptop you must use the native Linux **apt-get** package manager. You can run the following command on the terminal to install the needed dependencies:
```
sudo apt-get update
sudo apt-get install git python3-h5py python3-ipython python3-pint python3-sphinx python3-matplotlib python3-dev python3-numpy python3-scipy python3-pip build-essential gcc libhdf5-openmpi-dev 
```
Open, then, your ``.bashrc`` or ``.bash_profile`` file in your $HOME. For example, if you want to use the nano editor, type in the terminal:
```
nano $HOME/.bashrc
```
Add the following lines at the end of the file:
```
export PYTHONEXE=python3
export HDF5_ROOT_DIR=/usr/lib/x86_64-linux-gnu/hdf5/openmpi
```
If you'd like to use Python by using the shortcut ```python``` add also:
```
alias python=python3
```
Source the new bash profile by launching the following command on the terminal:
```
source $HOME/.bashrc
```

### Fedora OS
To install the dependencies on your Fedora-based laptop you must use the native Linux **dnf** package manager. You can run the following command on the terminal to install the needed dependencies:
```
sudo dnf install gcc-c++ git hdf5-openmpi hdf5-openmpi-devel openmpi-devel python python-devel python3-h5py ipython python3-pint python3-sphinx python3-matplotlib 
```
Open your ``.bashrc`` or ``.bash_profile`` file in your $HOME. For example, if you want to use the nano editor, type in the terminal:
```
nano $HOME/.bashrc
```
Add the following lines at the end of the file:
```
module load mpi
export HDF5_ROOT_DIR=/usr/lib64/openmpi/
```
If you'd like to use Python by using the shortcut ```python``` add also:
```
alias python=python3
```
Source the new bash profile by launching the following command on the terminal:
```
source $HOME/.bashrc
```

### ArchLinux OS
To install the dependencies on your ArchLinux-based laptop you must use the native Linux **pacman** package manager. You can run the following command on the terminal to install the needed dependencies:

```
sudo pacman -S git hdf5-openmpi python-numpy python-sphinx python-h5py-openmpi python-matplotlib python-pint make gcc 
```

### For all Distros
If you encounter problems, you may need to install openmpi and/or hdf5 directly from source. To do that, try to follow the instructions [here](https://smileipic.github.io/Smilei/Use/install_linux.html#troubleshooting).

### MacOS 
First install `xcode-select` by launching the following command on the terminal:
```bash
xcode-select --install
```
and then Homebrew via:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Once installed, to use Homebrew on the command line it is necessary to modify the ".zprofile" on your home by running following commands:
```bash
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/<your_account>/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)""
```
Then install git and Python using Homebrew:
```bash
brew install git python
brew install numpy scipy 
```
To use the installed Python as the default one you will need to modify the ".zprofile" adding the following line:
```bash
export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"
```
the path may change, use the one shown at the end of the installation. Once Python has been installed on your Laptop you have to create a virtual environment on your home to be able to install the python packages via pip:

``` Bash
python3 -m venv myenv
```
then, if you want to, let the terminal source it automatically every time you open a new terminal by adding to your ".zshrc" file the following line:

```
source ~/myenv/bin/activate
```
Alternatively, use the same line directly on the command line of your terminal. Source the environment and install the packages via pip:
```
pip install h5py ipython pint sphinx matplotlib dev numpy scipy 
```
Then, follow the related instructions for each case.

To run efficiently in parallel on your machine you need to know your architecture.
For example, you can find out the number of threads per core and cores per socket on your machine with the command: `lscpu` (Linux) or `sysctl -a | grep machdep.cpu` (MacOS).

# Cineca
You must have a Cineca account and two-factor authentication (2FA) enabled (https://wiki.u-gov.it/confluence/display/SCAIUS/How+to+connect+via+2FA).

To access Galileo100:
```bash
ssh <username>@login.g100.cineca.it
```
and Leonardo:
```bash
ssh <username>@login.leonardo.cineca.it
```
then follow the related instructions. 

# Git 
There are many tutorials online, please consider this just a summary/reminder of the main git commands.

If you want to contribute to the `PIC_tools` repo, first fork it in your GitHub account, then clone it: 
```bash
git clone git@github.com:<your_git_username>/PIC_tools.git
```
to incorporate changes from a remote repository into the current branch: 
```bash
git pull
```
to prepare the content staged for the next commit:
```bash
git add <files_to_add>
```
create a new commit, i.e. record the latest changes of the source code to your repository:
```bash
git commit -a -m "useful description"
```
update remote repository:
```bash
git push
```

If you want to merge your changes in the main repository, go to GitHub and make a pull request:
If the pull request is accepted and the code is merged, then go back to your repo and synch your fork, then do git pull from the terminal to update your remote repository. 
