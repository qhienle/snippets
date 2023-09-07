# Cheat Sheet

My collection of code snippets, templates and cheatsheets.

## Specialty Stuff

### aws

Setup configuration file `.aws/credentials`

    [default]
    aws_access_key_id = cqgc-user-blah
    aws_secret_access_key = S3cret+4ccess_K3y

    [emedgene]
    aws_access_key_id = 4lphaNum3ric5tr1ng
    aws_secret_access_key = S3cret+4ccess_K3y

`aws s3 --profile emedgene ls --recursive --page-size 10000 s3://cac1-prodca-emg-auto-results/CHU_Sainte_Justine/`

### Phenotips

URL: https://chusj.phenotips.com/
Username: CHUSJProdAPIUser
Password: Jeec4koh9uuce4kongei

Base64 Authorization: Q0hVU0pQcm9kQVBJVXNlcjpKZWVjNGtvaDl1dWNlNGtvbmdlaQo=
Secret Header: LstKPNP7XPXVYqq29qSh7MPpbCqB3dAYvoQpE7C4DHzo9tnz

Example curl command:
`curl -i -H "Authorization: Basic Q0hVU0pQcm9kQVBJVXNlcjpKZWVjNGtvaDl1dWNlNGtvbmdlaQo=" -H "X-Gene42-Secret: LstKPNP7XPXVYqq29qSh7MPpbCqB3dAYvoQpE7C4DHzo9tnz" https://chusj.phenotips.com/rest/patients/P0000001`

The following commands refer to the old database and are now deprecated.

`curl --user qhienle:<password> http://phenotips.chusj.org/get/PhenoTips/ExportPatient?id=P0000792 | python -m json.tool`
`jq`
 
```bash
for p in P0000792 P0000041 P0000765 P0000719 P0000381 P0000736; do
    curl  --user <username:password> http://phenotips.chusj.org/get/PhenoTips/ExportPatient?id=${p} > /staging2/data/Illumina/TSS/2021-03-08/json/pheno_json/${p}.json
done
```

### Illumina

For BaseSpace CLI

```bash
bs authenticate
# Lookup and retrieve RunID. 
bs list runs
# 210426_A00516_0213_AHY7VMDMXX | 205917719 | Seq_S2_JM_ValiCNV_20210426 | Complete |
# If on beluga, wrap in sbatch script
bs download run -i 205917719 -o 210426_A00516_0213_AHY7VMDMXX
```

Inspect the available parameters and options to build a command and launch an App on BSSH:

`bs -c cac1 launch application -n "TruSight Software Suite Connect" --app-version 1.1.0 --list`
    +------------------+----------------+-----------+-------------------------+-------------+----------+
    |      Option      |      Type      |  Choices  |         Default         | Multiselect | Required |
    +------------------+----------------+-----------+-------------------------+-------------+----------+
    | app-session-name | TextBox        | <String>  | Example [LocalDateTime] | false       | true     |
    | sample-id        | SampleChooser  | <Sample>  |                         | true        | true     |
    | project-id       | ProjectChooser | <Project> |                         | false       | true     |
    +------------------+----------------+-----------+-------------------------+-------------+----------+

Group all fastq for a biosample into a folder that we will upload. Then choose a BSSH Project ID into which to upload.

```bash
declare -a samples=(15411 15412 15413)
for sample in "${samples[@]}"; do
   mkdir "$sample"
   mv ${sample}_* ${sample}
done

bs -c cac1 project list #| grep EMG
```
 +----------------------------------------+---------+----------------+
 |                  Name                  |   Id    |   TotalSize    |
 +----------------------------------------+---------+----------------+
 | BSSH2TSS                               | 388391  | 0              |
 | Rapidomics                             | 665669  | 0              |
 | EMG                                    | 3772785 | 654311610010   |
 | Test                                   | 1814813 | 0              |

```bash
projectId=3772785
bs -c cac1 dataset upload --recursive --description 'GM180239' --project ${projectId} --biosample-name "15411" 15411
bs -c cac1 dataset upload --recursive --description 'GM180745' --project ${projectId} --biosample-name "15412" 15412
bs -c cac1 dataset upload --recursive --description 'GM180272' --project ${projectId} --biosample-name "15413" 15413

WORKDIR="./icitte"
mkdir -p ${WORKDIR}
cd ${WORKDIR}

for biosample in 15411 15412 15413; do
    for id in $( bs -c cac1 biosamples content --name ${biosample} --terse ); do
        bs -c cac1 file download --id ${id}
    done
done
```

Use the web [API](https://support-docs.illumina.com/SW/TSSS/TruSight_SW_API/Content/SW/FrontPages/TruSightSoftware_API.htm), _e.g._:

    curl -X GET "https://<domain-name>.<instance>/tms/api/v1/testDefinitions"
    -H "accept: application/json" -H "Authorization: APIKey <API Key>" -H "X-ILMN-Workgroup: <workgroup ID>"
    -H "X-ILMN-Domain: <domain name>"

```bash
curl -X GET "https://chusj.cac1.trusight.illumina.com/tms/api/v1/testDefinitions" \
-H "accept: application/json" -H "Authorization: APIKey R_YKxkVq)!Be_bJ%vRm" -H "X-ILMN-Workgroup: <workgroup ID>"
-H "X-ILMN-Domain: <domain name>"

curl -X GET "https://ilmn-demo.trusight.illumina.com/tms/api/v1/testDefinitions" \
-H "accept: application/json" -H "Authorization: APIKey Gsgeeg5SGU7IgZ4hwd" \
-H "X-ILMN-Workgroup: 5a2307ac-04c1-3e0f-a1f1-ab96c6edd0fc" -H "X-ILMN-Domain: ilmn-demo"
```

For TSS, the [CLI](https://support.illumina.com/help/TruSight_Software_Suite_1000000110864/Content/Source/Informatics/VariantSW/TSSS/CLI_swTSIS.htm) is mainly used for transfer/management operations on WGS files. 

`java -jar /staging2/soft/wgs-cli-2.0.1/wgs-cli-2.0.1.jar --help`

    Usage: wgs-cli.jar [-hV] [--configFilePath=<configFile>] [COMMAND]
    WGS-CLI Tool for file operations
        --configFilePath=<configFile>
                    Path to the uploader configuration file.
                    Defaults to ~/.illumina/uploader-config.json
    -h, --help      Show this help message and exit.
    -V, --version   Print version information and exit.
    Commands:
    help       Displays help information about the specified command
    configure  Configure wgs-cli tool
    fastqs     Upload fastq files for the specified Sample
    stage      Stage fastq files for specified folder name
    list       List fastq files for specified folder name
    download   Download a set of files matching a provided path expression
    delete     Delete fastq files for the specified sample
    vcfs       Upload vcfs files for the specified caseId

For TSS

[TSS Web API](http://support-docs.illumina.com/SW/TSSS/TruSight_SW_API/Content/SW/FrontPages/TruSightSoftware_API.htm)

```bash
# Get a list of all cases
curl --location --request GET 'https://chusj.cac1.trusight.illumina.com/crs/api/v2/cases/search?displayId=%25' \
--header 'X-Auth-Token: APIKey *#u37t_5KmQ4FWGfBl)Y)1' \
--header 'X-ILMN-Domain: chusj' \
--header 'X-ILMN-Workgroup: 42948014-b206-320d-b304-1af26fc98af3'

# Get a vcf file (fails)
curl -X GET "https://chusj.cac1.trusight.illumina.com/crs/api/v1/cases/01304558-a23b-4bd2-abe3-5b64443d18a0/files/01304558-a23b-4bd2-abe3-5b64443d18a0.repeats.merged.vcf.gz" \
    -H "caseid: 01304558-a23b-4bd2-abe3-5b64443d18a0" \
    -H "fileid: 01304558-a23b-4bd2-abe3-5b64443d18a0.repeats.merged.vcf.gz" \
    -H "X-Auth-Token: APIKey *#u37t_5KmQ4FWGfBl)Y)1'" \
    -H "X-ILMN-Workgroup: 42948014-b206-320d-b304-1af26fc98af3" \
    -H "X-ILMN-Domain: chusj"
```

#### tss-cli

#### Transferts avec `tss-cli`

Download and install `tss-cli-2.5.0` from TSS account, under _Download CLI Tool_ in the menu _Account_ (_c.f._ [Guide](https://support.illumina.com/help/TruSight_Software_Suite_1000000110864/Content/Source/Informatics/VariantSW/TSSS/CLI_swTSIS.htm#)). Copy the jar file to `beluga.calculquebec.ca:${HOME}/bin/` or wherever you want your bins.

```bash
java -jar ~/bin/tss-cli-2.1.0.jar configure --domain chusj --workgroup 42948014-b206-320d-b304-1af26fc98af3 --url chusj.cac1.trusight.illumina.com --apiKey 'R_YKxkVq)!Be_bJ%vRm'
# On spxp-app02, use:
# /staging2/soft/jdk-18.0.2/bin/java -jar /staging2/soft/tss-cli-2.2.0.jar --help
```

[On-line help for importing fastq with `tss-cli`](https://support.illumina.com/help/TruSight_Software_Suite_1000000110864/Content/Source/Informatics/VariantSW/TSSS/ImportFiles_swTSIS.htm)

Prepare a local folder for staging the transfer. `tss-cli` needs to have all the fastq for a sample in the same folder. 

```bash
cd $SCRATCH
flowcell="201222_A00516_0182_AHLH35DSXY" # 190605_A00516_0042_AHK7MMDSXX 201028_A00516_0166_AHNYMMDMXX 201211_A00516_0179_AHNWJJDRXX
for i in $(grep "TruSeq" ${flowcell}/SampleSheet.csv | grep -P "^1," | cut -d "," -f 2); do 
    echo "Processing ${i}";
    mkdir -p _fastq/${i}
    mv _fastq/${flowcell}/TruSeq_DNA_PCR-free/${i}*.fastq.gz _fastq/${i}/
done
```

`tss-cli` also needs a "manifest" in JSON [[ref.](https://support-docs.illumina.com/SW/TSSS/TruSight_SW_Suite/Content/SW/TSSS/SampleManifestJSON.htm)]. 

```json
{
    "files": [
        {
            "lane": "1",
            "library": "TruSeq_DNA_PCR-free",
            "read1": "/scratch/hien/_fastq/14126/14126_S1_L001_R1_001.fastq.gz",
            "read2": "/scratch/hien/_fastq/14126/14126_S1_L001_R2_001.fastq.gz",
            "readGroup": "14126_L001"
        },
        {
            "lane": "2",
            "library": "TruSeq_DNA_PCR-free",
            "read1": "/scratch/hien/_fastq/14126/14126_S1_L002_R1_001.fastq.gz",
            "read2": "/scratch/hien/_fastq/14126/14126_S1_L002_R2_001.fastq.gz",
            "readGroup": "14126_L002"
        },
        {
            "lane": "3",
            "library": "TruSeq_DNA_PCR-free",
            "read1": "/scratch/hien/_fastq/14126/14126_S1_L003_R1_001.fastq.gz",
            "read2": "/scratch/hien/_fastq/14126/14126_S1_L003_R2_001.fastq.gz",
            "readGroup": "14126_L003"
        },
        {
            "lane": "4",
            "library": "TruSeq_DNA_PCR-free",
            "read1": "/scratch/hien/_fastq/14126/14126_S1_L004_R1_001.fastq.gz",
            "read2": "/scratch/hien/_fastq/14126/14126_S1_L004_R2_001.fastq.gz",
            "readGroup": "14126_L004"
        }
    ]
}
```

```bash
# cd ${SCRATCH}/_fastq/
module load java/11.0.2
for sample in 14048 14049 14050; do
    python ~/bin/tss/make_fastq_manifest.py ${SCRATCH}/_fastq/${sample} > ${SCRATCH}/_fastq/${sample}/${sample}.json
    java -jar ~/bin/tss-cli-2.1.0.jar samples create --manifest ${SCRATCH}/_fastq/${sample}/${sample}.json --verbose --sample-id ${sample} &
done
```

Use the option `--overwrite` if you get the error "sample already exists".


#### ica

# Install

_C.f._ "TSS_data_repatriation_instructions.docx". Unzip and copy the `ica` and `ica.exe` onto the machine's directory, `~/bin/ica` for Linux.

```bash
# Authenticate
cd ~/bin
ica config set
```

    Creating /home/hienle/.ica/config.yaml
    Initialize configuration settings [default]
    server-url [use1.platform.illumina.com]: cac1.platform.illumina.com
    domain [None]: chusj
    server-url [cac1.platform.illumina.com]: cac1.platform.illumina.com
    domain [chusj]: chusj
    output-format [table]: table

```bash
ica login
# If first time, `ica` returns a url to which we must connect and accept the EULA
ica workgroups enter CHUSJ
# List GDS path for every case
ica folders list gds://wgs-aa9ccc8-2303-40d0-9775-8fca8605204e/42948014-b206-320d-b304-1af26fc98af3/cases/ --nonrecursive | cut -f2
# List "VCF" files in a folder
ica files list gds://wgs-aa9ccc8-2303-40d0-9775-8fca8605204e/42948014-b206-320d-b304-1af26fc98af3/cases/2b068565-5aa1-4430-bb14-9325e8197206/fwa.e94ba223298a4cc68f3a1b5a1763f070/19065-small-variants/ --nonrecursive | cut -f2 | grep vcf
# Download files
ica files download ${gds_path_to_file} /staging2/temp/emg/downloads/ --num-workers 6
```

With these two listing commands, we can re-construct the filesystem structure. 

    gds://wgs-aa9c6cc8-2303-40d0-9775-8fca8605204e/42948014-b206-320d-b304-1af26fc98af3/ (c.f. ingestionResult['result']['analysisInfo']['outputVolume'/'outputFolder'])
        L cases
            L case['id'] (ex: 2b068565-5aa1-4430-bb14-9325e8197206)
                L analysis['id'] (ex: fwa.e94ba223298a4cc68f3a1b5a173f070) a.k.a. case['ingestionResult']['jobId']
                    L sample-analysis (ex:19065-small-variants)
                        L 19065.cnv.vcf.gz
                        L files...
                    L 19066-small-variants
                        L 19066.cnv.vcf.gz
                        L ...
                    L 19067-small-variants
                        L 19065.cnv.vcf.gz
                        L ...
            L case_id...
                L analysis_id...
                    L ...
                    L ...
        L samples
            L 1713
                L 17135_S1_L001_R1_001.fastq.gz
                L 17135_S1_L001_R2_001.fastq.gz
                L 17135_S1_L002_R1_001.fastq.gz
                L 17135_S1_L002_R2_001.fastq.gz
            L 17136
                L ...
            L 17137
            L ...


#### Emedgene

Add participants:

https://{env}.emedgene.com/api/test/{EMG_ID}/add_participants_on_create/
Method: PUT
Payload:
```json
{"emails":["valid_email_address"]}
```

```python
import requests
def main():
    test_data = {}

    # Please note - the Authorization header is only valid for a limited time, and
    # expires after 8H. In that case, any request made with an expired token will 
    # return a 403 code.
    # To resolve it - just re-do the Login procedure to get a new token.
    #
    url      = "https://chusaintejustine.emedgene.com/api/auth/api_login/"
    payload  = '{"username": "cqgc.bioinfo.hsj@ssss.gouv.qc.ca", "password": "7TmbuM3TUCMwP"}'
    headers  = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    auth_header = response.json()["Authorization"]
    print(auth_header)
    requests.post('https://chusaintejustine.emedgene.com/api/test/',
                json={'test_data': test_data},
                headers={'Authorization': auth_header})

if __name__ == '__main__':
    main()
```

### Convert BCL to FASTQ

```bash
dragen --bcl-conversion-only true \
    --bcl-input-directory /mnt/spxp-app02/staging/hiseq_raw/200302_A00516_0106_BHNKHFDMXX \
    --output-directory /mnt/spxp-app02/staging2/dragen/200302_A00516_0106_BHNKHFDMXX \
    --sample-sheet /mnt/spxp-app02/staging/hiseq_raw/200302_A00516_0106_BHNKHFDMXX/Seq_S2_JM_20200302.csv \
    --force \
    >> /mnt/spxp-app02/staging2/dragen/200302_A00516_0106_BHNKHFDMXX/200302_A00516_0106_BHNKHFDMXX.dragen.bcl2fastq.out \
    2>> /mnt/spxp-app02/staging2/dragen/200302_A00516_0106_BHNKHFDMXX/200302_A00516_0106_BHNKHFDMXX.dragen.bcl2fastq.out
```

`--sample-sheet`: Path to Sample Sheet is optional if the `SampleSheet.csv` file is in the `--bcl-input-directory directory`.
`--force`: If `--output-directory` already exists.


## Python

```bash
python -m json.tool --help
python -m json.tool --indent 2 response.json
```

On Windows, with mambaforge installed: `C:\Windows\system32\cmd.exe "/K" C:\Users\lequa000\AppData\Local\mambaforge\Scripts\activate.bat C:\Users\lequa000\AppData\Local\mambaforge`

Or: `powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'C:\Users\lequa000\AppData\Local\mambaforge\shell\condabin\conda-hook.ps1' ; conda activate 'C:\Users\lequa000\AppData\Local\mambaforge' "` (Need to first run `conda init powershell` in a Conda cmd.exe prompt?) 
C:\Users\lequa000\AppData\Local\mambaforge\Scripts\conda.exe ?

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



### Plotly

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
#SBATCH --mail-user=quang-hien.le.hsj@ssss.gouv.qc.ca
#SBATCH --mail-type=ALL
#SBATCH --output=/scratch/hien/%x.log

echo "Hello world!"
```

### DRAGEN

DRAGEN server is spxp-app04. Connect to it directly using your Windows login, or from spxp-app02: `qrsh -now no -p 10`

```bash
dragen --help
```

Create a hash table for the human genome, version hg19, while enabling CNV and RNA-Seq analyses.

```bash
sudo mkdir -p /mnt/spxp-app02/staging2/raw/hg38.hash_table.cnv
sudo chown lequa000:share hg38.hash_table.cnv
sudo chmod ug+rwx hg38.hash_table.cnv
dragen \
    --build-hash-table true \
    --ht-reference /staging/human/reference/hg38.BroadInstitute/Homo_sapiens_assembly38.fasta \
    --output-directory /mnt/spxp-app02/staging2/raw/hg38.hash_table.cnv/ \
    --enable-cnv true \
    --enable-rna true \
    --ht-alt-liftover /opt/edico/liftover/bwa-kit_hs38DH_liftover.sam
```

