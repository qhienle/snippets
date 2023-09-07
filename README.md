# Cheat Sheet

My collection of code snippets, templates and cheatsheets.

## Python

```bash
python -m json.tool --help
python -m json.tool --indent 2 response.json
```

On beluga.calculquebec.ca, additional modules are needed.

`module load StdEnv/2020 scip-stack/2020b`

Jupyter Notebook on beluga. Adjust values of parameters as needed.

```bash
ssh beluga.calculquebec.ca
source .venv-jupyter/bin/activate
salloc --job-name "Jupyter" --time=3:0:0 --ntasks=1 --cpus-per-task=2 --mem-per-cpu=2048M --account=def-rallard srun $VIRTUAL_ENV/bin/notebook.sh
```

On localhost, open an SSH tunnel to view the remote Jupyter Notebook in a local web browser.

`sshuttle --dns -Nr <username>@<cluster>.calculquebec.ca`

### conda

Conda [cheatsheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).

Command                                 | Description
----------------------------------------|------------- 
`conda info`                            | Verify conda is installed, check version number
`conda update conda`                    | Update package named conda  
`conda update --all`                    | Update all packages
`conda env list`                        | Install package pandas Get a list of all my environments, active environment is shown with `*`
`conda create --name py39 python=3.9`   | Create a new environment named "py9", install Python 3.9
`conda list`                            | List all packages and versions installed in active environment
`conda activate py39`                   | Activate environment 'py39' to use it
`conda search`                          | Use conda to search for a package
`conda install pandas`                  | Install package pandas
`conda install --help`                  | Get help on sub-command `install`
`conda deactivate`                      | Deactivate the current environment
`conda env remove --name py39`          | Delete an environment and everything in it

### venv

Create a `.venv` folder within the working directory, from where binaries and libraries will be executed.

```bash 
mkdir workdir && cd workdir
python3 -m venv .venv
source .venv/bin/activate
which python
python --version
```

Install libraries, develop, analyze... _e.g._ For viewing [Plotly](https://plotly.com/python/getting-started/) outputs within Jupyter Lab notebooks:

```bash
pip install pandas
pip install plotly==4.14.1`
pip install jupyterlab "ipywidgets>=7.5"
# JupyterLab renderer support
jupyter labextension install jupyterlab-plotly@4.14.1`
# OPTIONAL: Jupyter widgets extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.14.1
```

Exit the virtual environment:

`deactivate`

### Pandas

Select rows where column contains _pattern_ `df['colname'].str.contains('pattern')`

### IPython/Jupyter

`jupyter-lab --ip=10.128.80.26 --no-browser`

Save variables and sessions with _magic_
`%store var`/`%store -r var`, `%history` or `notebook` 


## Git/GitHub

to get Git-Bash working on a Windows 10 administered by IT and not connected on a work network. $HOEM is not set and $HOMEDRIVE is set to a network drive. Either delete the network drive `net use U: /delete` or

```cmd
# OK for git-bash, but not for VSCode
set HOME=C:\Users\lequa000\
set HOMEDRIVE=C:
C:/Users/lequa000/AppData/Local/Programs/Git/bin/bash.exe -i -l
```

Cache credentials for one day `git config --global credential.helper "cache --timeout=86400"`

- 1 hour: `cache --timeout=3600`
- 1 day:  `cache --timeout=86400`
- 1 week: `cache --timeout=604800`

Or use a platform-specific Git Credentials Manager


## Linux stuff

Cheat sheet for Linux Shell (Bash) stuff.

### ssh

https://superuser.com/questions/555799/how-to-setup-rsync-without-password-with-ssh-on-unix-linux

```bash
# 1. Test rsync over ssh (with password):
rsync -avz -e ssh /home/test/ user@192.168.200.10:/backup/test/

# 2. ssh-keygen generates keys. Note: When it asks you to enter the passphrase 
# just press enter key, and do not give any password here.
ssh-keygen

# 3. ssh-copy-id copies public key to remote host
ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.200.10

# 4. Perform rsync over ssh without password
ssh user@192.168.200.10
rsync -avz -e ssh /home/test/ user@192.168.200.10:/backup/test/
```

### screen

```bash
screen -S [session_name]
screen -ls # list opened sessions
screen -dr [screen -r [[pid.]tty[.host]]
```

While in a screen session: ^A (Control-A) for issuing commands

- ^A^d: Detach screen
- ^A^c: Create new screen
- ^A^a: Switch between current and last screen (or p=previous, n=next)
- ^A ": List active screens of current session
- ^A C: Clear screen
- ^A A: Allow to set window title 

Escape screen commands: ^A + litteral key

- _e.g._ Beginnning of prompt ^A-a
- _e.g._ End of prompt ^A-e 

Split `screen` _windows_ into separate _panes_

- ^A S: Horizontal split or ^A | (pipe) for vertical
- ^A TAB: switch between panes (then create a new window with ^A c)
- ^A Q: Quit all panes except active one, or ^A X to eXit the current one 

### tmux

Or use tmux (not on all systems)

```bash
tmux new -s SessionName
tmux detach
tmux ls
tmux attach -t [SessionName]
```
General commands (Ctrl+b,...):
- ?: Help!
- $: Rename current session
- s: List Sessions
- c: Create new window
- ,: Ctrl+b :rename-window <new_name> or tmux rename-window <new_name> 
- w: List Windows
- n: Display Next window
- p: Display Previous window
- [0-9]: Display Numbered Window
- d: Detach session

Pane commands (Ctrl+b,...): 
- %: Create a horizontal split.
- “: Create a vertical split.
- h,i,j,k or Arrow keys: Move to the pane on the left, up, down or right.
- q: Briefly show pane numbers.
- ;: Toggle between the current and previous pane
- o: Move through panes in order. Each press takes you to the next, until you loop through all of them.
- }: Swap the position of the current pane with the next.
- {: Swap the position of the current pane with the previous.
- x: Close the current pane.


### SLURM

[Compute Canada Wiki for running jobs](https://docs.computecanada.ca/wiki/Running_jobs)
[Status of Compute Canada Servers](https://status.computecanada.ca/)

For interactive jobs, graphical programs can be run by adding --x11 flag to your salloc command. In order for this to work, you must first connect to the cluster with X11 forwarding enabled (see the SSH page for instructions on how to do that). Note that an interactive job with a duration of three hours or less will likely start very soon after submission as we have dedicated test nodes for jobs of this duration. Interactive jobs that request more than three hours run on the cluster's regular set of nodes and may wait for many hours or even days before starting, at an unpredictable (and possibly inconvenient) hour.

```bash
# Interactive jobs, allocated faster if rquest is less than 3 hours
salloc --account def-rallard --job-name "InteractiveJob" --cpus-per-task 2 --mem-per-cpu 2000  --time 3:0:0
srun --account def-rallard --job-name "InteractiveJob" --cpus-per-task 2 --mem-per-cpu 2000 --time 4:00:00 --pty bash

# Load a module
module avail scipy
module spider r
module load  

# Submit a job
sbatch [-a def-rallard] script_name
squeue -u $USER
```

Different tools available for monitoring jobs and the system. Use information from `squeue` to list jobs and monitor jobs.

```bash

# See running jobs
squeue -u $USER [--iterate 3]
scontrol show job JOBID
sstat --jobs=your_job-id --format=jobid,cputime,maxrss,ntasks
sstat --helpformat
sinfo
smap
# See running jobs with ssh -Y
sview

# Monitor resources for a running job
squeue -u $USER
# Note the node on which our job of interest is running
ssh NODE
htop -u $USER
top -u $USER

# See past jobs
sacct

```

Script configuration

```bash
#!/bin/bash

#SBATCH --time=25:00:00
#SBATCH --account=def-rallard
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --job-name=200918_A00516_0160_AHMHGGDRXX_archive
#SBATCH --mail-user=someone@somewhere.com
#SBATCH --mail-type=ALL
#SBATCH --output=${SCRATCH}/%x.log

echo "Hello world!"
```
