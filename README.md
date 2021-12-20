# Demultiplexing

## Introduction
The script `demux.sh` demultiplexes fastqc files according to their indexes (barcodes). 

## Input
`demux.sh` requires five files, all of the fastq files are expected to be gzipped:
1. **Index file** -- A file containing a list of all the unique indexes used in the experiment.
2. **Read 1 file** -- A `fastq` file containing all the forward reads from an experiment.
3. **Index 1 file** -- A `fastq` file containing the indexes of the forward reads, each index must match the line of the corresponding forward read
4. **Read 2 file** -- A `fastq` file containing all the reverse reads from an experiment.
5. **Index 2 file** -- A `fastq` file containing the indexes of the reverse reads, each index must match the line of the corresponding reverse read
6. **Output directory** -- Desired output directory
7. **Q-score cutoff** -- If average Q-score of index is lower than this cutoff then the read is discarded
