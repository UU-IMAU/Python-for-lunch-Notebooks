# using Jupyter's LabApp or NotebookApp on Cartesius

*André Jüling (a.juling@uu.nl) | DEcember 2018*

## Step 0.

Get on Cartesius:

`ssh -Y dijkbio@cartesius.surfsara.nl`

and load a suitable python environment on Cartesius.

You can make your own conda environment by loading the easybuild environment and then Miniconda

`module load eb`

`module load Miniconda3`

`source activate {your-conda-environment}`

(see the [conda_and_environments](https://github.com/UU-IMAU/Python-for-lunch-Notebooks/blob/master/PFL1_virtual-environments/conda_and_environments.md) document in how to set that up)

---

# direct: Cartesius <-> whitelisted local machine

When you are at IMAU you can connect directly to cartesius.surfsara.nl, because the IP addresses here are on a whitelist.

## Step 1.

on Cartesius: activate Jupyterlab as
follows:

`jupyter lab --no-browser --port=8892`

you can alternatively run the NotebookApp by replacing `lab` with `notebook`

## Step 2.

on local machine: use this command to establish an ssh tunnel:

`ssh -N -f -L localhost:8895:localhost:8892`

## Step 3.

in the browser on the local machine type

`localhost:8895` 

There will be a prompt for your account password. Then you can work with Jupyterlab on Cartesius.

---

# indirect: Cartesius <-> gemini <-> local machine

When you are working on a non-whitelisted computer, you can ssh tunnel via gemini.

## Step 1.

on cartesius: as Step 1 above

## Step 2.

get on gemini

`ssh -Y {your-solis-ID}@gemini.science.uu.nl`

there establish an ssh connection to cartesius:

`ssh -N -L 8800:localhost:8892 dijkbio@cartesius.surfsara.nl`

## Step 3.

on your local machine connect to gemini:

`ssh -N -f -L localhost:8895:localhost:8800 {your-solis-ID}@gemini.science.uu.nl`

## Step 4.

on local machine: as step 3 above



NB. The numbers 88xx are chosen to be large enough integers, but are essentially random.