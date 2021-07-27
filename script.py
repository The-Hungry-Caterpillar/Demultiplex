import bioinfo
import numpy as np

convert=bioinfo.convert_phred


def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "still need description")
	#parser.add_argument('- command line variable', '-- python variable', description)
	parser.add_argument('-f', '--input_file', help='filename for input')
	parser.add_argument('-k', '--kmer_length', type=int, help='input kmer length')
	#parser.add_argument('-o', '--output_file', help='file to output data')
	#parser.add_argument('-t', '--title', help='category, i.e. velvet kmersize 31')
	return parser.parse_args()

args=get_args()


def make_empty_array (file): #counts the number of records in a fastq file and the length of each record and makes an array of corresponding size
	f=open(file, 'r')
    
	length=0
	width=0
	n=0
    
	while True:
		line=(f.readline()).strip()

		if line == '':
			break

		if n % 4 == 3:
			length += 1
			width = len(line) #can probably find a more computationally friendly way to make this variable
		
		n+=1

	f.close()
	
	array = np.zeros((length, width)) #creates an array where there is a list for each position in the read and the number of these lists is the number of records in the file

	return(array) #returns empty array of length=#records and width=#of bases


def populate_array(file):
    
    f=open(file,'r')
    
    current_record = 0 
    n = 0
    
    while True:
        
        line=f.readline()

        if n%4==3: #if the file line is 3,7,11... i.e. the quality score line
    
            for position in range(len(array[0])): #for each charcter in the quality score line
        
                array[position,current_record] = convert(line[position])
            
            current_record += 1
                
        if line=='': #if there are no more lines to read, break
            break
        
        n += 1
    
    f.close()
    

################## This section calls the appropriate functions to build a mean quality score distribution graph #################

file=args.input_file

array=make_empty_array(file)

populate_array(file)

