# Linux Cheat Sheet

My collection of various code snippets, templates, and command cheat sheets for Linux Shell (Bash) stuff.

## Shell

Config files `.bashrc` and `.bash_profile` are read by "interactive" shells (as in, ones connected to a terminal, or pseudo-terminal in the case of, say, a terminal emulator running under a windowing system). `.bashrc` is only read by a shell that's both interactive and non-login, so you'll find most people end up telling their `.bash_profile` to also read .bashrc with something like

`[[ -r ~/.bashrc ]] && . ~/.bashrc`

### `zsh` peculiarities

## Specialty programmes

### Git/GitHub

to get Git-Bash working on a Windows 10 administered by IT and not connected on a work network. $HOME is not set and $HOMEDRIVE is set to a network drive. Either delete the network drive `net use U: /delete` or

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
