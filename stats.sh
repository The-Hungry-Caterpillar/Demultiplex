#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

conda activate bgmp_py39
dir=buckets
sdir=/projects/bgmp/shared/2017_sequencing
total=$(gunzip -c $sdir/1294_S1_L008_R1_001.fastq.gz|grep -c '^@K00337')
ls -1 | grep 'read1' | while read file
do
wc -l $dir/$file >> data
done
python stats.py -n $total