#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

shared_dir=/projects/bgmp/shared/2017_sequencing

index2=$shared_dir/1294_S1_L008_R3_001.fastq.gz

/usr/bin/time -v \
python ../count_good_qual.py \
-f $index2 \
-l 8 \
-Q 38