# Scitas
Scripts or tips for running on EPFL SCITAS 

## 1. Introduction to the SCITAS cluster

The SCITAS cluster is a high-performance computing (HPC) cluster at EPFL. It is a shared resource that is available to all EPFL researchers. The cluster is composed of several nodes, each with multiple cores and a large amount of memory. The cluster is managed by the SCITAS team, who are responsible for maintaining the hardware and software, as well as providing support to users. More information about the SCITAS cluster can be found on the [SCITAS website](https://www.epfl.ch/research/facilities/scitas/) and in the [SCITAS user guide](https://scitas-doc.epfl.ch/).

For our use and this repository, we will focus on the following aspects of the SCITAS cluster:
- ***Jed*** cluster (***@jed.epfl.ch***) is the one we used
- 2 directories are used 
    - `/scratch/{user}/` for temporary storage, no storage limit, but files are deleted after [15/30](https://scitas-doc.epfl.ch/storage/file-system/#occupancy-limits) days. 
        - All files after 30 days will be deleted
        - If with high occupancy, files may be deleted after 2 weeks. but files within 2 weeks seems to be safe
    - `/home/{user}` for login in and running scripts, 100GB limit, data will be erased after two years of inactivity or 6 months after leaving EPFL, whichever occurs first.

## 2. Useful commands

### 2.1. Terminal Setup

It is recommended to use the Ubuntu terminal to connect to the SCITAS cluster. Following the [instructions on Windows](https://learn.microsoft.com/en-us/windows/wsl/install) to install the WSL linux terminal. Or we can also use the ***Git Bash*** terminal (Powershell terminal could also work for logging in, but the command `rsync` doesn't work, you should use `scp` instead, but it would be much slower).

To install `rsync` for Git Bash terminal, see [here](https://prasaz.medium.com/add-rsync-to-windows-git-bash-f42736bae1b3) for more details.

### 2.2. Useful commands and links

- **Login to the SCITAS cluster**: 

    [https://scitas-doc.epfl.ch/user-guide/using-clusters/connecting-to-the-clusters/](https://scitas-doc.epfl.ch/user-guide/using-clusters/connecting-to-the-clusters/)  
    ```bash
    ssh {user}@jed.epfl.ch
    ```
- **Introduction to Linux commands**:
    
    [https://www.epfl.ch/research/facilities/scitas/documentation/training/#intro](https://www.epfl.ch/research/facilities/scitas/documentation/training/#intro)

# 3. Running Jobs on the SCITAS cluster with python
Here we will show how to run jobs on the SCITAS cluster using python. We will use the `paramiko` library to connect to the cluster and run commands.






