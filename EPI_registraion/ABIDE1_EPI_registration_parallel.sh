#!/bin/bash

#SBATCH --job-name=ABIDE1_EPI
#SBATCH --partition=256GB
#SBATCH --nodes=5
#SBATCH --ntasks=120
#SBATCH --time=0-12:00:00
#SBATCH --workdir=
#SBATCH --output="logs/slurm_%j.txt"\
CORES_PER_TASK=2

now=$(date +"%m-%d-%Y,%H:%M:%S")
echo "Job start: $now"

module load parallel
module load slurm
module load python/3.7.x-anaconda
source activate CondaEnv

SRUN_CMD="srun --exclusive -N1 -n1 -c $CORES_PER_TASK"
TASK_CMD="python ANTsRegistraionMeanTemplate.py"

# get the input files that are in the native space(ignore files that have -space in them  as they are not in native space)
x=$(ls <path_to>/ABIDEI/derivatives/CPAC/output/cpac_cpac-custom-nuisance/*/func/*mean_bold.nii.gz | grep -v "_space-")

parallel --joblog "logs/$SLURM_JOB_ID.task.log" $SRUN_CMD $TASK_CMD {} ::: $x
