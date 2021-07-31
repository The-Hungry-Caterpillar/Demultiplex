#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

shared_dir=/projects/bgmp/shared/2017_sequencing

index1=$shared_dir/1294_S1_L008_R2_001.fastq.gz

/usr/bin/time -v \
python ../count_good_qual.py \
-f $index1 \
-l 8 \
-Q 35