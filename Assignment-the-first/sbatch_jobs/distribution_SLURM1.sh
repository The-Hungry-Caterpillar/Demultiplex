#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

shared_dir=/projects/bgmp/shared/2017_sequencing
plot_dir=/projects/bgmp/jogata/bioinformatics/bi622/Demux/distribution_plots

conda activate bgmp_py39

index1=$shared_dir/1294_S1_L008_R2_001.fastq.gz

#records=$(gunzip -c $index1 |grep -c '^@K00337')

/usr/bin/time -v \
python ../mean_quality_distribution.py \
-f $index1 \
-l 8 \
-nr 363246735 \
-t index1_mean_Qscores \
-d $plot_dir