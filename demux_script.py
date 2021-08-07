import bioinfo
import gzip

def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "still need description")
	#parser.add_argument('- command line variable', '-- python variable', description)
	parser.add_argument('-f', '--input_file', help='filename for input')
	parser.add_argument('-bd', '--bucket_directory', help='input directory to which buckets will be added, INCLUDE THE / AT THE END, OTHERWISE THE CODE WILL NOT WORK')
	parser.add_argument('-r1', '--read1', help='input read1 file')
	parser.add_argument('-i1', '--index1', help='input index1 file')
	parser.add_argument('-i2', '--index2', help='input index2 file')
	parser.add_argument('-r2', '--read2', help='input read2 file')
	
	#parser.add_argument('-l', '--read_length', type=int, help='input read length')
	#parser.add_argument('-nr', '--number_records', type=int, help="input number of records, use this command to count: ~$ records=$(grep -c '^@K00337' <filename>)'")
	#parser.add_argument('-t', '--plot_title', help = 'input desired distribution plot title')
	#parser.add_argument('-d', '--directory', help= 'input directory to save plots')
	return parser.parse_args()

args=get_args()


nucleotide_string='ACGGT'
print(bioinfo.reverse_compliment(nucleotide_string))

def open_buckets():
	buckets_dictionary={#Index read (i.e. AACTGACG): open(<bucket_out_file>, 'w')
	}
	#want to make another dictionary for matching reverse reads
	rbuckets_dictionary={}
	f = open('test_files/indexes', 'r')
	lines=(f.readlines())
	for line in lines[1:]:
		buckets_dictionary[(line.strip()).split('\t')[4]] =  open(args.bucket_directory+((line.strip()).split('\t')[4]) + '_read1', 'w')
		rbuckets_dictionary[bioinfo.reverse_compliment((line.strip()).split('\t')[4])] =  open(args.bucket_directory+((line.strip()).split('\t')[4]) + '_read2', 'w')
		#open(args.bucket_directory+((line.strip()).split('\t')[4]) + '_read1', 'w')
		#open(args.bucket_directory+((line.strip()).split('\t')[4]) + '_read2','w')
	
	f.close()

	buckets_dictionary['BQ_read1']=open('bad_quality_read1','w')
	buckets_dictionary['Index_swap_read1']=open('index_swap_read1','w')
	
	rbuckets_dictionary['BQ_read2']=open('bad_quality_read2','w')
	rbuckets_dictionary['Index_swap_read2']=open('index_swap_read2','w')

	return(buckets_dictionary, rbuckets_dictionary)


buckets=open_buckets()[0] #creates the read1 buckets
rbuckets=open_buckets()[1] #creates the read2 buckets

#these open the files to be read
r1=open('R1.fastq','r') #read 1
i1=open('R2.fastq','r')	#index 1
i2=open('R3.fastq','r') #index 2
r2=open('R4.fastq','r') #read 2



while True:
	
	n=0

	#read the first line of a record in each file, make one of them a temp header
	header = r1.readline().strip().split('')[0] #also strip off the stuff at the end that's not common amongst all four headers
	i1.readline().strip()
	i2.readline().strip()
	r2.readline().strip()


	#read the second line of a record in each file (the sequence)
	read1 = r1.readline().strip()
	index1 = i1.readline().strip()
	index2 = i2.readline().strip()
	read2 = r2.readline().strip()


	#read the third line of a record in each file (the plus sign)
	r1.readline().strip()
	i1.readline().strip()
	i2.readline().strip()
	r2.readline().strip()


	#read the fourth line of a record in each file (the quality scores)
	read1_qual = r1.readline().strip()
	index1_qual = i1.readline().strip()
	index2_qual = i2.readline().strip()
	read2_qual = r2.readline().strip()

	if ('N' in index1) or ('N' in index2):
		buckets[index1].write(header+index1+index2) #append header to index_output_file_read1

	if r2.readline() == '':
		break
""" 		#index_file_dictionary[index1][0].write(read1) #append sequence to index_output_file_read1
		#index_file_dictionary[index1][0].write('+') #append plus sign
		#index_file_dictionary[index1][0].write(read1_qual) #append the quality score line to index_output_file_read1

		#now let's take care of read 2...
		index_file_dictionary[index1][1].write(header+index1+index2) #append header to index_output_file_read2
		index_file_dictionary[index1][1].write(read2) #append sequence to index_output_file_read2
		index_file_dictionary[index1][1].write('+') #append plus sign
		index_file_dictionary[index1][1].write(read2_qual) #append quality score line to index_output_file_read2


	if index1 == bioinfo.reverse_compliment(index2): #this will append the read 1 record to the appropriate index file if the indexes match
		
		#let's put the read1 record in the appropriate file
		index_file_dictionary[index1][0].write(header+index1+index2) #append header to index_output_file_read1
		index_file_dictionary[index1][0].write(read1) #append sequence to index_output_file_read1
		index_file_dictionary[index1][0].write('+') #append plus sign
		index_file_dictionary[index1][0].write(read1_qual) #append the quality score line to index_output_file_read1

		#now let's take care of read 2...
		index_file_dictionary[index1][1].write(header+index1+index2) #append header to index_output_file_read2
		index_file_dictionary[index1][1].write(read2) #append sequence to index_output_file_read2
		index_file_dictionary[index1][1].write('+') #append plus sign
		index_file_dictionary[index1][1].write(read2_qual) #append quality score line to index_output_file_read2


	if index1 != reverse_compliment(index2): #if the indexes don't match...

		then do the same thing as the if loop directly above, but put the records in the index_swapped files




	if r2.readline() == '':
		break

	n+=1

	if n % 21367455 ==0: #this prints out progress every 216367455 lines (1/17th), note that this number needs to be changed depending on input file if you want to keep it nice
		print('working on record {}, we are {}/17th of the way there!'.format(n/4, n/4))
 """