# Managing Python Packages

The availability of thousands of open source packages is one of the great strengths of Python. You could install them yourself, but it is much handier to have a package management system take care of it for you (including keeping track of all dependencies). There a several systems, such as `pip`, `Canopy`, and `(Ana)conda`. We show here how to work with Conda, but the other package management systems should be able to do most of the same things. We recommmend using Miniconda.

# Conda package managment system

Conda is an open source package management system and environment management system that runs on Windows, macOS and Linux. Conda quickly installs, runs and updates packages and their dependencies.

It is bundled with two principal distributions:

### Miniconda

Free minimal installer, it includes conda, Python, their dependencies on and a few others. __(~ 400 MB)__

https://conda.io/miniconda.html

### Anaconda

It includes conda, Python and 100+ scientific packages and their dependencies. __(~ 3 GB)__

https://www.anaconda.com/download/#macos

## How to install packages

Open a terminal and type

`conda install packagename`

### Installing and channels

Anaconda also maintains a separate channel of packages, which is the default one.

It might happen that the package you need is not on the default channel. You can install it from another channel , specifying it every time you install a package:

`conda install -c channel-name packagename`

If you find yourself using the same channel often, then you might want to add it to your configuration.

`conda config --append channels channel-name`

One of the most common channels is `conda_forge`.


## Conda on clusters

### Cartesius

to load the conda package manager on Cartesius, first load the easybuild module and then Miniconda3

`module load eb`

`module load Miniconda3`


### Gemini and Hopf

... people are working on it ...



# What is a conda environment and why you want to use it

A folder or directory that __contains a specific collection of conda packages__ and their dependencies, so they can be maintained and __run separately without interference__ from each other. 

Why conda environments are so convenient:

- you want to share some code and __make everyone able to use it__

- you want to share some code with the future self and __make yourself able to use it__

- you want to use your code on a __different machine__

- you are very fond of a package which exists only for a __specific version of python__

- you __don't__ want to __mess up with your system__ python

## Basic commands for environments

- Create new environment, with a specific version of python (it will use the base (Ana)conda python otherwise)

`conda create --name myenv`

- ... with a specific version of python

`conda create -n myenv python=3.5`

- Activate and deactivate environments (on Windows you omit "source")

`source activate myenv`

`source deactivate`

- View a list of your environments

`conda env list`

- Install packages in the environment from the root environment

`conda install -n myenv scipy=0.15.0`

- or from the environment after having activated it

`conda install scipy=0.15.0

- locate the directory for the conda environment (on Windows omit `echo`) 

`echo $CONDA_PREFIX`


## Jupyter notebook in conda environments

- Install jupyter in your environment

`conda install jupyter`

- Install nb_conda in your environment

`conda install nb_conda`

## Play with your environments

## Clone environments

- You may want to clone your environment

`conda create --name myclone --clone myenv`

- or export it (to use it on another machine)

`conda env export > myenv.yml`

- Once you have the _yml_ file you can copy it to the desired machine and recreate there your environment

`conda env create -f myenv.yml`

- Cross-platform

`conda env export --no-builds > myenv.yml`

# What if something goes wrong

- Remove packages

`conda remove packagename`

- Backup of previous states of your environment

`conda list --revisions`

`conda install --revision N`

The whole history of your environment is saved in the file

`<environment-path>/conda-meta/history`

- Delete environment

`conda remove --name myenv --all`

# More information at

https://conda.io/docs/
