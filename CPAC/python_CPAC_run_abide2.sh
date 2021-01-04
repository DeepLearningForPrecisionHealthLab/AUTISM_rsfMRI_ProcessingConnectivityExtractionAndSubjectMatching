#!/bin/bash
#
#SBATCH --job-name abide2_1113sub   # python_CPAC_run_10Subjects
#SBATCH --partition 256GB    # partition (queue)
#SBATCH --nodes 1
#SBATCH --time 20-0:0:0

# The standard output and errors from commands will be written to these files.
# %j in the filename will be replace with the job number when it is submitted.
#SBATCH -o /project/bioinformatics/DLLab/STUDIES/ABIDE2/CPAC/Jbs/sub1113/log/job_%j.out
#SBATCH -e /project/bioinformatics/DLLab/STUDIES/ABIDE2/CPAC/Jbs/sub1113/log/job_%j.err




# We do not specify -ntasks since CPAC spawns its own threads.

# COMMAND GROUP 1
source activate /project/bioinformatics/DLLab/distribution/PipelineCondaEnvironments/cpacEnv

# COMMAND GROUP 2
python /project/bioinformatics/DLLab/distribution/PipelineCondaEnvironments/cpacEnv/bin/cpac_run.py  /project/bioinformatics/DLLab/STUDIES/ABIDE2/CPAC/Jbs/sub1113/pipe-cpac-abide_slurmv1.yml /project/bioinformatics/DLLab/STUDIES/ABIDE2/CPAC/Jbs/sub1113/rerun_sub.yml

# END OF SCRIPT
