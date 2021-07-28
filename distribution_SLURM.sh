#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

shared_dir=/projects/bgmp/shared/2017_sequencing
plot_dir=/projects/bgmp/jogata/bioinformatics/bi622/Demux/distribution_plots

conda activate bgmp_py39

read1=$shared_dir/1294_S1_L008_R1_001.fastq.gz
records=$(grep -c '^@K00337' $read1)

/usr/bin/time -v \
python $plot_dir/mean_quality_distribution.py \
-f $read1 \
-l 101 \
-nr $records \
-t read1_mean_Qscores \
-d $plot_dir


index1=$shared_dir/1294_S1_L008_R2_001.fastq.gz
records=$(grep -c '^@K00337' $index1)

/usr/bin/time -v \
python $plot_dir/mean_quality_distribution.py \
-f $index1 \
-l 8 \
-nr $records \
-t index1_mean_Qscores \
-d $plot_dir


index2=$shared_dir/1294_S1_L008_R3_001.fastq.gz
records=$(grep -c '^@K00337' $index2)

/usr/bin/time -v \
python $plot_dir/mean_quality_distribution.py \
-f $index2 \
-l 8 \
-nr $records \
-t index2_mean_Qscores \
-d $plot_dir


read2=$shared_dir/1294_S1_L008_R4_001.fastq.gz
records=$(grep -c '^@K00337' $read2)

/usr/bin/time -v \
python $plot_dir/mean_quality_distribution.py \
-f $read2 \
-l 101 \
-nr $records \
-t read2_mean_Qscores \
-d $plot_dir
