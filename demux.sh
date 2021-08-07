#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

sdir=/projects/bgmp/shared/2017_sequencing

conda activate bgmp_py39

/usr/bin/time -v \
python demux_script.py \
-i $sdir/indexes.txt \
-bd buckets/ \
-r1 $sdir/1294_S1_L008_R1_001.fastq.gz \
-i1 $sdir/1294_S1_L008_R2_001.fastq.gz \
-i2 $sdir/1294_S1_L008_R3_001.fastq.gz \
-r2 $sdir/1294_S1_L008_R4_001.fastq.gz