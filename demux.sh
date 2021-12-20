#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1


# help functions, displays user options
help()
{
    echo "This script takes five files and uses them to demultiplex a set of fastq files."
    echo " "
    echo "The following five files are required:"
    echo "     -i     Path to file containing list of unique indexes"
    echo "     -r1    Path to file containing first reads"
    echo "     -r2    Path to file containing second reads"
    echo "     -i1    Path to file containing first read indexes (indexes must correlate line-for-line with first reads)"
    echo "     -i2    Path to file containing second read indexes (indexes must correlate line-for-line with second reads)"
    echo " "
    echo "The following options are also required:"
    echo "     -o     Path for output directory (will create one folder per index)"
    echo "     -q     Input average qscore cutoff"
}

# process input options
while getopts ":hi:r1:r2:i1:i2:o:q:" option
do
    case $option in 
        
        h) #displays help
            help
            exit;;

        i) #enter index file
            i=$OPTARG;;

        r1) #enter read1 file
            r1=$OPTARG;;

        r2) #enter read2 file
            r2=$OPTARG;;

        i1) #enter index1 file
            i1=$OPTARG;;
   
        i2) #enter index2 file
            i2=$OPTARG;;
           
        o) #enter output directory
            o=$OPTARG;;

        q) #enter quality score cutoff
            q=$OPTARG;;
            
        \?) #displays invalid option
            echo "Error: Invalid option(s)"
            exit;;

    esac
done

def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "still need description")
	#parser.add_argument('- command line variable', '-- python variable', description)
	parser.add_argument('-i', '--index_file', help='filename for input')
	parser.add_argument('-bd', '--bucket_directory', help='input directory to which buckets will be added, INCLUDE THE / AT THE END, OTHERWISE THE CODE WILL NOT WORK')
	parser.add_argument('-r1', '--read1', help='input read1 file')
	parser.add_argument('-i1', '--index1', help='input index1 file')
	parser.add_argument('-i2', '--index2', help='input index2 file')
	parser.add_argument('-r2', '--read2', help='input read2 file')
	parser.add_argument('-Q', '--qscore', type=int, help='input average qscore cutoff')
  

# conda activate bgmp_py39
mkdir -q $o

/usr/bin/time -v \
python demux_script.py \
-i $i \
-bd $o \
-r1 $r1 \
-i1 $i1 \
-i2 $i2 \
-r2 $r2 \
-Q $q

dir=$o
touch $o/data_Qscore$q
ls -1 $o | grep 'read1' | while read file
do
wc -l $o/$file >> data_Qscore$q
done

python stats.py -f data_Qscore$q -Q $q
