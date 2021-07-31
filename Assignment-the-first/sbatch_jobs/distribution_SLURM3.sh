#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

shared_dir=/projects/bgmp/shared/2017_sequencing
plot_dir=/projects/bgmp/jogata/bioinformatics/bi622/Demux/distribution_plots

conda activate bgmp_py39

read2=$shared_dir/1294_S1_L008_R4_001.fastq.gz

records=$(gunzip -c $read2 |grep -c '^@K00337')

/usr/bin/time -v \
python ../mean_quality_distribution.py \
-f $read2 \
-l 101 \
-nr $records \
-t read2_mean_Qscores \
-d $plot_dir