
# Running Jupyter notebooks from Gemini
*Leo van Kampenhout (L.vankampenhout@uu.nl) \
December 2018*

## Step 1. 
On Gemini, install jupyter notebook through [conda](https://conda.io/miniconda.html) or another package manager 

```
conda install jupyter
```

Add any other packages that you might need. \
Alternatively, skip this step and use my existing Python 3.7 installation @ `/home/staff/kampe004/miniconda3`


## Step 2. 
Start a jupyter notebook server. 

```bash 
export PATH=/home/staff/kampe004/miniconda3/bin:$PATH # modify if needed
source activate base
jupyter notebook --no-browser --ip=`hostname`
```

or execute this bash wrapper script: 

```
sh /home/staff/kampe004/start_jupyter.sh
```

Something along these lines will appear:

```
[I 15:11:37.774 NotebookApp] Serving notebooks from local directory: /home/staff/kampe004
[I 15:11:37.774 NotebookApp] The Jupyter Notebook is running at:
[I 15:11:37.774 NotebookApp] http://science-bs35:8888/?token=3461515385e60d2794fb4403f9036d225598192cb6bd1e52
[I 15:11:37.775 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 15:11:37.775 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://science-bs35:8888/?token=3461515385e60d2794fb4403f9036d225598192cb6bd1e52
```

The number `8888` and the token will be needed later. 

### ProTip
Start the server process inside [GNU screen](https://en.wikipedia.org/wiki/GNU_Screen) to keep it running even if your SSH session disconnects.

## Step 3.
On the client machine (your laptop / desktop), connect to the running server using this SSH tunneling command:

```bash
ssh -N -l kampe004 -L 8890:science-bs35:8888 science-bs35.science.uu.nl
```

replace `kampe004` with your own SolidID and `8888` with the port that was displayed earlier, if that differs from mine. 
The target port is this example is `8890` which should be available. No need to change that. 
You'll be asked for your password. Then, if the process does not abort, the connection is made and ready to use. 

Windows users: have a look here: https://www.skyverge.com/blog/how-to-set-up-an-ssh-tunnel-with-putty/

## Step 4.
Fire up your browser (e.g. Firefox) and navigate to `http://localhost:8890/tree`

Enter the token that was reported in step 2. You should now be good to go. 

## Closing down
First, close all running notebooks and kernels the normal way. \
Then, abort the SSH tunnel on the client machine using Ctrl-C. \
Then, abort the Jupyter server on the server machine (gemini) using Ctrl-C.


