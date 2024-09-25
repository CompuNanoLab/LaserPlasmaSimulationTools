# Laptop

In order to use most of the Laser-Plasma simulation tools you need a Unix machine (Linux or MacOS). Follow the instructions below for your OS.

## Setup a Linux sub-system in Windows
In Windows, you must set up a running Linux sub-system:

- Go to Start. Search for "Turn Windows features on or off." (For laptops set up in Italian look for "Attiva o disattiva funzionalità di Windows")
- Check the option "Windows Subsystem for Linux" ("Sottosistema Windows per Linux"):
  
  <img src="/PiC_Tools/Images/322772146-75fe59a8-35c6-47c9-9b3e-fef7ff2c0fad.png" width="400" />
  
- Open **Command Prompt** (**Prompt dei Comandi**) as an administrator:
  
  <img src="/PiC_Tools/Images/322772777-96052034-10c0-417a-90dc-71180df4704d.png" width="400" />
  
- Run the command below to install the *Distro* (suggested ones: *Debian* or *Ubuntu*) of your choice:
  ```
  wsl --install -d <Distro>
  ```
- Launch the *Distro* by searching from the start menu and insert a username and password. Remember that when you launch the virtual machine you are opening a terminal in the ```$HOME``` of your Linux platform.
  
  <img src="/PiC_Tools/Images/327967584-fb762f06-3d6b-4ddc-b090-e2569d73d3fa.png" width="400" />

You can access the files of your virtual machine by opening the **Windows File Explorer** (**Esplora File**) and looking for the Linux folder (i.e. the penguin folder). Inside the folder with the name of your Distro you can find your ```home``` directory.

<img src="/PiC_Tools/Images/327968742-3278d5b3-cbc6-43a3-959e-78b11d40ac9a.png" width="600" />

Follow then the instructions for the *Distro* that you chose.

## Before starting

Here is a list of basic useful commands that you can use in a Unix terminal:

```
    cat --- for creating and displaying short files
    chmod --- change permissions
    cd --- change directory
    clear --- clear screen
    cp --- for copying files
    diff --- compares files
    echo --- echo argument
    grep --- search file
    head --- display first part of file
    history --- show history of previous commands
    ls --- see what files you have
    less --- use to read files (q to exit)
    man --- view manual pages for Unix commands
    more --- use to read files
    mkdir --- create directory
    mv --- for moving and renaming files
    pwd --- find out what directory you are in
    rm --- remove a file
    rmdir --- remove directory
    setenv --- set an environment variable
    sort --- sort file
    tail --- display last part of file
    tar --- create an archive, add or extract files
    wc --- count characters, words, lines
    who --- tells you who's logged on

```

To edit files you can use a command-line editor like `nano`. To open a file using `nano`, open your terminal and type the following command:

```bash
nano text.txt
```
Then, you can move with arrow keys and edit the file as you want. Use **Ctrl + O + enter** to save changes to the fileand **Ctrl + X** to exit. Other available editors are `vi` and `emacs`. 

To run efficiently in parallel on your machine you need to know your architecture.
For example, you can find out the number of threads per core and cores per socket on your machine with the command: `lscpu` (Linux) or `sysctl -a | grep machdep.cpu` (MacOS).

## General dependencies
This section contains the instructions to install general dependencies in your laptop based on your OS. These dependencies are required by all Laser-Plasma tools.

### Debian-based (Ubuntu) OS
To install the dependencies on your Debian-based laptop you must use the native Linux **apt-get** package manager. You can run the following command on the terminal to install the needed dependencies:
```
sudo apt-get update
sudo apt-get install git python3-h5py python3-dev python3-numpy python3-scipy build-essential gcc libhdf5-openmpi-dev 
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
Follow then the istructions in **For all Distros** section.

### Fedora OS
To install the dependencies on your Fedora-based laptop you must use the native Linux **dnf** package manager. You can run the following command on the terminal to install the needed dependencies:
```
sudo dnf install gcc-c++ git hdf5-openmpi hdf5-openmpi-devel openmpi-devel python python-devel python-numpy python-scipy
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
Source the new bash profile by launching the following command on the terminal:
```
source $HOME/.bashrc
```
Follow then the istructions in **For all Distros** section.

### ArchLinux OS
To install the dependencies on your ArchLinux-based laptop you must use the native Linux **pacman** package manager. You can run the following command on the terminal to install the needed dependencies:
```
sudo pacman -S git hdf5-openmpi python-numpy python-scipy make gcc 
```
Follow then the istructions in **For all Distros** section.

### For all Distros
Create then a `python` virtual environment in your `$HOME` by running:
``` Bash
cd 
python -m venv myenv
```
then, source it to activate the virtual environment. In Linux:

``` Bash
source ~/myenv/bin/activate
```
In Windows:
``` Bash
source /home/your_username/myenv/bin/activate
```
and install the needed packages via pip:
``` Bash
pip3 install h5py ipython pint sphinx matplotlib dev numpy scipy 
```
If you want to, let the terminal source the environment automatically every time you open a new terminal by adding to your ".bashrc" file the following line:

``` Bash
source ~/myenv/bin/activate
```
Otherwise, any time you want to use `python` activate the environment by launching in the terminal the source prompt. If you want to deactivate the virtual environment you'll need to run the command:
``` Bash
deactivate 
```

If you encounter problems with openmpi and/or hdf5, you may need to install them from source. To do that, try to follow the instructions [here](https://smileipic.github.io/Smilei/Use/install_linux.html#troubleshooting).

### MacOS 

The easiest way to install the necessary dependencies is by using alternatively **Homebrew**. First install `xcode-select` by launching the following command on the terminal:
```bash
xcode-select --install
```
and then Homebrew via:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Once installed, to use Homebrew on the command line you need to modify the ".zprofile" on your home by running following commands:
```bash
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/<your_account>/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)""
```
Then install some basic dependencies using Homebrew:
```bash
brew update
brew install git python
brew install numpy scipy
brew install openmpi
brew install hdf5-mpi
brew install libomp
```
To check the formulae (dependencies) installed on your Mac use the command
```
brew list
```
To check the version of your C++ compiler use the command:
```
brew info gcc
``` 
To use the installed Python as the default one you will need to modify the ".zprofile" adding the following line (you can use `nano` editor to do that):
```bash
export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"
```
the path may change, use the one shown at the end of the installation. Once Python has been installed on your Laptop you have to create a virtual environment on your home to be able to install the python packages via pip:

``` bash
python3 -m venv myenv
```
then, if you want to, let the terminal source it automatically every time you open a new terminal by adding to your ".zshrc" file the following line:

``` Bash
source ~/myenv/bin/activate
```
Alternatively, use the same line directly on the command line of your terminal. Source the environment and install the packages via pip:
``` Bash
pip install h5py ipython pint sphinx matplotlib dev numpy scipy 
```
If you want to deactivate the virtual environment you'll need only to run the command:
``` Bash
deactivate 
```

# Git 
There are many tutorials online, please consider this just a summary/reminder of the main git commands.

If you want to contribute to the `LaserPlasmaSimulationTools` repo, first fork it in your GitHub account, then clone it: 
```bash
git clone git@github.com:<your_git_username>/LaserPlasmaSimulationTools.git
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
