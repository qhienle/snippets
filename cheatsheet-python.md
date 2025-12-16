# Python Cheat Sheet

My collection of code snippets, templates and cheatsheets.

## Modules

```bash
python -m json.tool --help
python -m json.tool --indent 2 response.json
```

## Environments

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

### IPython/Jupyter Notebook on spxp-app02.

```bash
ssh -L 8080:localhost:8080 ${USER}@spxp-app02
screen -S dev # Protect jupyter server from hangups
conda activate CQGC-utils
jupyter lab --no-browser --port 8080 --notebook-dir ~/bin
# Paste URL from STDOUT into localhost browser
```

Save variables and sessions with _magic_
`%store var`/`%store -r var`, `%history` or `notebook` 


