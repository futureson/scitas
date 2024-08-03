import os
import time
import shutil
import paramiko

def generate_slurm_script(user, crop, gim, scenario):
    slurm_script = f"""#!/bin/sh
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH --time 72:00:00
#SBATCH --mem=60G
#SBATCH -e slurm-%j.err
#SBATCH -o slurm-%j.out
#SBATCH --mail-type=end
#SBATCH --mail-user=qiming.sun@epfl.ch
RUN=/scratch/{user}
cd $RUN/CODE

module load matlab/R2024a

# time matlab -nodisplay -r "mainp('Wheat','CWatM','historical')"; 
time matlab -nodisplay -r "mainp({crop!r},{gim!r},{scenario!r})"; 

exit;"""
    output_file = 'torun/' + crop[0:3] + '_' + gim[0:2] + scenario[3:5] + '.job'
    jobfile = crop[0:3] + '_' + gim[0:2] + scenario[3:5] + '.job'
    with open(output_file, 'w', newline= '\n') as file: # newline= '\n' is used to fit the linux format
        file.write(slurm_script)
    print(f"SLURM job script '{output_file}' created successfully.")
    return jobfile

def connect(user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = 'jed.epfl.ch', username=user, password=password)
    return ssh

def check_job_status(ssh, user):
    stdin, stdout, stderr = ssh.exec_command(f"squeue -u {user}")

    # print the status of the jobs in good format
    status = stdout.read().decode().split('\n')
    # if status is not empty, meaning the jobs are running
    if status:
        print('Jobs are running')
    else:
        print('No jobs running')

    return status

def upload_data(ssh, user, gim, i, gim_path_prefix):
    local_gim_path = gim_path_prefix + gim + '/'
    remote_gim_path = f'{user}@jed.epfl.ch:/scratch/{user}/CODE/ALL_elabs_ISIMIP/OutputData/water_global/{gim}'
    remote_dir= f'/scratch/{user}/CODE/ALL_elabs_ISIMIP/OutputData/water_global'
    if i == 0:
        ssh.exec_command(f'rm -r {remote_dir}')
        ssh.exec_command(f'mkdir {remote_dir}')
    # check if the remote directory exists
    stdin, stdout, stderr = ssh.exec_command(f'ls {remote_gim_path.split(":")[-1]}')
    if 'No such file or directory' in stderr.read().decode():
        print('All files needs upload')
        os.system(f'powershell.exe scp -r {local_gim_path} {remote_gim_path}') # upload through powershell scp needs ssh key setup otherwise it will ask for password and wait a long time
    else:
        print('Remote data already exists')

def submit_job(ssh, user, gim, crops_torun, scenarios):
    # every time generate the slurm script for 1 gim, 2 crops and 4 scenarios until all crops are done
    jobs = []
    for crop in crops_torun:
        for scenario in scenarios:
            jobfile = generate_slurm_script(user, crop, gim, scenario)
            # copy the slurm script to the server
            sftp = ssh.open_sftp()
            sftp.put(f'torun/{jobfile}', f'/home/{user}/{jobfile}')
            sftp.close()

            # run the slurm script
            stdin, stdout, stderr = ssh.exec_command(f'sbatch {jobfile}')
            time.sleep(1) # wait for 1 second before checking the job status

            # move the job file to running directory locally
            shutil.move(f'torun/{jobfile}', f'running/{user}/{jobfile}')
            jobs.append(jobfile)
    print(f"The following jobs are running: {jobs}")

# def download_results(ssh, user, local_res_path):

#     stdin, stdout, stderr = ssh.exec_command(f"squeue -u {user}")
#     status = stdout.read().decode().split('\n')

#     remote_res_path = f'{user}@jed.epfl.ch:/scratch/{user}/CODE/SIM_RESULTS/*'
#     if status[1:-1] == []:
#         print('Jobs are Done')
#         os.system(f'powershell.exe scp -r {remote_res_path} {local_res_path}')
#         print('Results are downloaded')
#         # ssh.exec_command(f"rm -r {remote_res_path}")
#         # archive all jobs when Status is empty
#         ssh.exec_command("mv *.job *.err *.out finished")
#         jobs = os.listdir(f'running/{user}')
#         for jobfile in jobs:
#             shutil.move(f'running/{user}/{jobfile}', f'finished/{user}/{jobfile}')
#     else:
#         print('Jobs are Running')

# def run(user, password, gim, interval = 3600, crops, scenarios, gim_path_prefix, local_res_path):

#     ssh = connect(user, password)

#     for i in range(0,4):
#         crops_torun = crops[2*i:2*(i+1)]
#         print('crops to run:', crops_torun)

#         upload_data(ssh, user, gim, i, gim_path_prefix)
        
#         submit_job(ssh, user, gim, crops_torun, scenarios)

#         check_job_status(ssh, user, interval, i, local_res_path) # check every hour and download data when finished 
