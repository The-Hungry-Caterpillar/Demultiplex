import bioinfo
import gzip
import numpy as np

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
	
	return parser.parse_args()

args=get_args()

#for testing purposes:
# python3 demux_script.py -bd buckets/ -r1 test_files/R1.fastq -i1 test_files/R2.fastq -i2 test_files/R3.fastq  -r2 test_files/R4.fastq


def open_buckets():
	'''Creates buckets based on indexes'''
	buckets_dictionary={#Index1 read (i.e. AACTGACG): (handle(i.e. B1), open(<bucket_out_file_read1>, 'w', count)
	}
	rbuckets_dictionary={#Index2 read (rev comp of index1): (handle(i.e. B1), open(<bucket_out_file_read2>, 'w', count)
	}
	f = open(args.index_file, 'r') #opens the list of indexes
	lines=(f.readlines())
	for line in lines[1:]:
		'''populates the above dictionaries as described'''
		buckets_dictionary[(line.strip()).split('\t')[4]] =  (((line.strip()).split('\t')[3]), open(args.bucket_directory+((line.strip()).split('\t')[4]) + '_read1', 'w'))
		rbuckets_dictionary[bioinfo.reverse_compliment((line.strip()).split('\t')[4])] =  (((line.strip()).split('\t')[3]), open(args.bucket_directory+((line.strip()).split('\t')[4]) + '_read2', 'w'))
	
	f.close()

	#creates bad_quality buckets
	buckets_dictionary['BQ_read1']=('bq1',open(args.bucket_directory+'bad_quality_read1','w'))
	rbuckets_dictionary['BQ_read2']=('bq2',open(args.bucket_directory+'bad_quality_read2','w'))
	
	#creates index_swapping buckets
	buckets_dictionary['Index_swap_read1']=('is1', open(args.bucket_directory+'index_swap_read1','w'))
	rbuckets_dictionary['Index_swap_read2']=('is2', open(args.bucket_directory+'index_swap_read2','w'))

	return(buckets_dictionary, rbuckets_dictionary)


buckets=open_buckets()[0] #creates the read1 buckets
rbuckets=open_buckets()[1] #creates the read2 buckets


#these open the files to be read
r1=gzip.open(args.read1,'rt') #read 1
i1=gzip.open(args.index1,'rt') #index 1
i2=gzip.open(args.index2,'rt') #index 2
r2=gzip.open(args.read2,'rt') #read 2



while True:
	'''This loop reads fastq files and sorts them into buckets '''
	
	n=1 #this little guy is for keeping track of progress

	if n % 21367455 ==0: #prints out progress every 216367455 lines (1/17th), note that this number needs to be changed depending on input file if you want to keep it nice
		print('working on record {}, we are {}/17th of the way there!'.format(n/4, n/4))


	####################### section 1 -- reading the records from each file ###########################

	#read the first line of a record in each file, make one of them a temp header
	header = r1.readline().strip().split(' ')[0] #also strip off the stuff at the end that's not common amongst all four headers
	i1.readline().strip()
	i2.readline().strip()
	r2.readline().strip().split(' ')


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


	if header == '':
		break

	############################# section 2 -- sort the records ##############################

	if ((index1 not in buckets) or (np.mean([bioinfo.convert_phred(n) for n in index1_qual])<35)) or ((index2 not in rbuckets) or (np.mean([bioinfo.convert_phred(n) for n in index2_qual])<35)):
		'''If the indexes contain Ns, or the average Qscore is less than 35, then put read1 and read2 records in their respective bad quality buckets'''

		print(header,index1,index2, sep=' ', file=buckets['BQ_read1'][1]) #adds header (with both indexes, not rev comp) to bad qual read1 bucket
		print(read1, file=buckets['BQ_read1'][1]) #adds read1 to bad qual read1 bucket
		print('+', file=buckets['BQ_read1'][1]) #adds the little plus sign to bad qual read1 bucket
		print(read1_qual, file=buckets['BQ_read1'][1]) #adds the quality score to the bad qual read1 bucket

		print(header,index1,index2, sep=' ', file=rbuckets['BQ_read2'][1]) #adds header (with both indexes, not rev comp) to bad qual read2 bucket
		print(read2, file=rbuckets['BQ_read2'][1]) # so on 
		print('+', file=rbuckets['BQ_read2'][1]) #and so forth
		print(read2_qual, file=rbuckets['BQ_read2'][1]) #...


	elif buckets[index1][0]==rbuckets[index2][0]: #recall that bucket keys are indexes and rbucket keys are rev comp indexes, but both have the same handle as value[0]
		''' If the handles of the indexes match then put each record in its respective index/read bucket'''
		
		print(header,index1,index2, sep=' ', file=buckets[index1][1]) #adds header (with both indexes, not rev comp) to bad qual read1 bucket
		print(read1, file=buckets[index1][1]) #adds read1 to bad qual read1 bucket
		print('+', file=buckets[index1][1]) #adds the little plus sign to bad qual read1 bucket
		print(read1_qual, file=buckets[index1][1]) #adds the quality score to the bad qual read1 bucket

		print(header,index1,index2, sep=' ', file=rbuckets[index2][1]) #adds header (with both indexes, not rev comp) to bad qual read2 bucket
		print(read2, file=rbuckets[index2][1]) # so on 
		print('+', file=rbuckets[index2][1]) #and so forth
		print(read2_qual, file=rbuckets[index2][1]) #...


	else:
		''' If the indexes are swapped, then put the records in the respective swapped files'''
	
		print(header,index1,index2, sep=' ', file=buckets['Index_swap_read1'][1]) #adds header (with both indexes, not rev comp) to bad qual read1 bucket
		print(read1, file=buckets['Index_swap_read1'][1]) #adds read1 to bad qual read1 bucket
		print('+', file=buckets['Index_swap_read1'][1]) #adds the little plus sign to bad qual read1 bucket
		print(read1_qual, file=buckets['Index_swap_read1'][1]) #adds the quality score to the bad qual read1 bucket

		print(header,index1,index2, sep=' ', file=rbuckets['Index_swap_read2'][1]) #adds header (with both indexes, not rev comp) to bad qual read2 bucket
		print(read2, file=rbuckets['Index_swap_read2'][1]) # so on 
		print('+', file=rbuckets['Index_swap_read2'][1]) #and so forth
		print(read2_qual, file=rbuckets['Index_swap_read2'][1]) #...


	n+=1

r1.close()
i1.close()
i2.close()
r2.close()

for key in buckets:
	buckets[key][1].close()

for key in rbuckets:
	rbuckets[key][1].close()


