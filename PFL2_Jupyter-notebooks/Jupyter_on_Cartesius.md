# using Jupyter's LabApp or NotebookApp on Cartesius

*André Jüling (a.juling@uu.nl) | December 2018*

## Step 0.

Get on Cartesius:

`ssh -Y {account}@cartesius.surfsara.nl`

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

on Cartesius: activate Jupyterlab as follows:

`jupyter lab --no-browser --port=8892`

you can alternatively run the NotebookApp by replacing `lab` with `notebook`

## Step 2.

on local machine: use this command to establish an ssh tunnel:

`ssh -N -L localhost:8895:localhost:8892 {account}@cartesius.surfsara.nl`

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

`ssh -N -L 8800:localhost:8892 {account}@cartesius.surfsara.nl`

## Step 3.

on your local machine connect to gemini:

`ssh -N -L localhost:8895:localhost:8800 {your-solis-ID}@gemini.science.uu.nl`

## Step 4.

on local machine: as step 3 above

---

## N.B.

- you may get an error message `bind: Cannot assign requested address`, this is not fatal in itself but is a warning that you can ignore
- The numbers 88xx are chosen to be large enough integers, but are essentially random.
- After some inactivity, the ssh pipes often break, which necessitates reestablishing them. This can be avoided using the [screen](https://www.gnu.org/software/screen/) functionality. See [here](http://aperiodic.net/screen/quick_reference) for a handy list of commands for `screen`.
- adding a `-f` flag will run the tunnel in th background
- use `ps aux | grep ssh` to see which ssh tunnels are active (and `kill -9 {processID}` to kill it)
- on Cartesius, there are two workspaces `int1` and `int2` to which you can directly connect by prepending `int1-bb` or `int2-bb` to `cartesius.surfsara.nl`, i.e. `ssh {cartesius-username}@int1-bb.cartesius.surfsara.nl`
