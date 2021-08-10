#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

sdir=/projects/bgmp/shared/2017_sequencing
q=33
conda activate bgmp_py39
mkdir buckets_Qcutoff$q

#/usr/bin/time -v \
python demux_script.py \
-i $sdir/indexes.txt \
-bd buckets_Qcutoff$q/ \
-r1 $sdir/1294_S1_L008_R1_001.fastq.gz \
-i1 $sdir/1294_S1_L008_R2_001.fastq.gz \
-i2 $sdir/1294_S1_L008_R3_001.fastq.gz \
-r2 $sdir/1294_S1_L008_R4_001.fastq.gz \
-Q $q

conda activate bgmp_py39
dir=buckets_Qcutoff$q
touch data_Q$q
ls -1 $dir | grep 'read1' | while read file
do
wc -l $dir/$file >> data_Q$q
done


python stats.py -f data_Q$q -Q $q