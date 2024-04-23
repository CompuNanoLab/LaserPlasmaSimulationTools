# Goal of these instructions
The aim is to help one build and run 3 particle-in-cell codes (WarpX, Smilei and EPOCH) on a laptop or on Cineca supercomputers.

# Laptop
## General dependencies
First, install on your laptop the following fundamental software:

For **Debian-based OS**:
```bash
sudo apt-get install git python3-h5py python3-ipython python3-pint python3-sphinx python3-matplotlib python3-dev python3-numpy python3-scipy python3-pip build-essential gcc libhdf5-openmpi-dev 
```

For **MacOS** first install Homebrew via:
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
source myenv/bin/activate
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
similar for Marconi100:
```bash
ssh <username>@login.m100.cineca.it
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
