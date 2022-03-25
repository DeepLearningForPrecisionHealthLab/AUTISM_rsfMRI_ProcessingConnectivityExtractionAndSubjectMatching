#!/bin/bash
#SBATCH --job-name=A1
#SBATCH --partition=32GB
#SBATCH --nodes=60
#SBATCH --ntasks=120
#SBATCH --time=3-00:00:00
#SBATCH --workdir="/archive/bioinformatics/DLLab/src/AlexTreacher/autism_DCG/cpac_pipeline/20210825_ABIDE_CPAC/ABIDEII"
#SBATCH --output="./logs/slurm-%j.out"
#SBATCH --exclude=NucleusA126

#currently, this needs to be set manually. I suggest looking at the data_config and searching for "- anat"
intNumSubjects=1114

# The number of cores per task = the number of cpus on the partition / (ntasks/nodes)
# Freesufer needs 4GB ram to run, thus I suggest running 8 jobs per node on the 32GB nodes.
# in this case the 32GB nodes have 32 physical cores, so 32/(80/10) = 4
CORES_PER_TASK=16

#load some env files
module load parallel
module load python
module load singularity/3.0.2
source activate Alex37CPAC

strPipeLineDir=/archive/bioinformatics/DLLab/src/AlexTreacher/autism_DCG/cpac_pipeline/20210825_ABIDE_CPAC/ABIDEII
TASK_SCRIPT='cpac run /project/bioinformatics/DLLab/STUDIES/ABIDE2/Source/ABIDEII-ALL /archive/bioinformatics/DLLab/AlexTreacher/data/20210825_ABIDE_CPAC/ABIDEII/derivatives/CPAC participant --pipeline_file /archive/bioinformatics/DLLab/AlexTreacher/src/autism_DCG/cpac_pipeline/20210825_ABIDE_CPAC/ABIDEII/pipeline_20210825.yml --platform singularity --data_config_file /archive/bioinformatics/DLLab/AlexTreacher/src/autism_DCG/cpac_pipeline/20210825_ABIDE_CPAC/ABIDEII/cpac_data_config_2021-08-25T18-00-51Z.yml --n_cpus 16 --mem_gb 16 --participant_ndx'

# set up for the parallel, give a max time incase it gets hung up (otherwise it would hog resources)
SRUN_CMD="srun --exclusive -D $strPipeLineDir -N1 -n1 -c $CORES_PER_TASK -t 10:00:00"

seq $intNumSubjects | parallel \
	--joblog ./logs/$SLURM_JOB_ID.tasklog.txt \
	-j $SLURM_NTASKS \
	--delay .2 \
	$SRUN_CMD $TASK_SCRIPT {}
