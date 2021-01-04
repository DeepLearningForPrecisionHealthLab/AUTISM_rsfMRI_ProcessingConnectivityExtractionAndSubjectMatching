#!/bin/bash

#SBATCH --job-name=ABIDE2_falff_Registration
#SBATCH --partition=32GB
#SBATCH --nodes=32
#SBATCH --ntasks=512
#SBATCH --time=0-05:00:00
#SBATCH --workdir="/project/bioinformatics/DLLab/Alex/Projects/Autism/dev"
#SBATCH --output="/project/bioinformatics/DLLab/Alex/Projects/Autism/data/EPI_Registration_mean_functional_EPI_masked/JobOutput/slurm_%j.txt"

now=$(date +"%m-%d-%Y,%H:%M:%S")
echo "Job start: $now"

module load parallel

# SRUN arguments
CORES_PER_TASK=2 # the number of CPU cores/number of jobs per node. EG if each node has 72 cores and you are running 4 jobs across 2 nodes, this would be 36

INPUTS_COMMAND="cat ../data/ABIDE2_Chosen_Scans.txt"

TASK_SCRIPT='python ANTsRegistraionMeanTemplateEPIMasked.py'

SRUN_CMD="srun --exclusive -N1 -n1 -c $CORES_PER_TASK"
PARALLEL_CMD="parallel --delay .2 -j $SLURM_NTASKS --joblog /project/bioinformatics/DLLab/Alex/Projects/Autism/data/EPI_Registration_mean_functional/JobOutput/$SLURM_JOB_ID.task.log"

# set up the lockfiles, it's important to do it here so it only gets done once!
module load python/3.6.4-anaconda
source activate /project/bioinformatics/DLLab/shared/CondaEnvironments/Alex366Nipype #activate a conda environment, it need to have filelock in it

# Run the jobs
eval $INPUTS_COMMAND | $PARALLEL_CMD $SRUN_CMD $TASK_SCRIPT 2 {}

now=$(date +"%m-%d-%Y,%H:%M:%S")
echo "Job End: $now"

