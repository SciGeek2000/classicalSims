#!/bin/bash
#SBATCH --job-name=sim_test_0
#SBATCH --account=taersevim
#SBATCH --partition=lr3
#SBATCH --qos=lr_normal
#SBATCH --nodes=4
#SBATCH --cpus-per-task=16
#SBATCH --time=0:05:00
#
## Command(s) to run (example):
module load bio/blast/2.6.0
module load gnu-parallel/2019.03.22

export WDIR=./scqubit_yamls
cd $WDIR

# set number of jobs based on number of cores available and number of threads per job
export JOBS_PER_NODE=$(( $SLURM_CPUS_ON_NODE / $SLURM_CPUS_PER_TASK ))
#
echo $SLURM_JOB_NODELIST |sed s/\,/\\n/g > hostfile
#
parallel --jobs $JOBS_PER_NODE --slf hostfile --wd $WDIR --joblog task.log --resume --progress -a task.lst sh run-blast.sh {} output/{/.}.blst $SLURM_CPUS_PER_TASK


#!/bin/bash
#SBATCH --job-name=test
#SBATCH --account=account_name
#SBATCH --partition=es1
#SBATCH --qos=es_normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#
# Processors per task (please always specify the total number of processors twice the number of GPUs):
#SBATCH --cpus-per-task=2
#
#Number of GPUs, this can be in the format of "gpu:[1-4]", or "gpu:V100:[1-4] with the type included
#SBATCH --gres=gpu:1
#
# Wall clock limit:
#SBATCH --time=1:00:00
#
## Command(s) to run (example):
./a.out