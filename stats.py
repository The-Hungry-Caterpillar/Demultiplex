def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "very nice script")
	parser.add_argument('-n', '--number_lines', help='input total number of records')
	return parser.parse_args()
args=get_args()
def distribution(x_data,y_data, print_to_terminal = False):
	'''input x_data and y_data and out comes a bargraph! Set True if you want the graph to pop up, otherwise it will just save as a png file'''
	import matplotlib.pyplot as plt
	plt.xlabel('Index handle', size=20)
	plt.ylabel('# fastq records in bucket', size=20)
	plt.title('Base Mean Quality Scores', size = 22)
	plt.bar(x_data,y_data, color='mediumspringgreen',width=1)
	plt.savefig('Distribution of fastq files (read1 only)')
	if print_to_terminal == True:
		plt.show()
index_swaps=0 #this will increase in the while loop -- used to calculate percentage of index_swaps
bad_quality=0 #this will increase in the while loop -- used to calculate percentage of bad quality
number_records=[] #this houses the number of records from each file
names=[] #this houses the handles of the records, i.e. B1_R1
f=open('data','r') # open file containing two columns; index handle, and number of LINES in that index bucket (for one read)
while True:
	line=f.readline().strip().split(' ') #will look like ["handle", "number of lines"]
	if line==['']:
		break
	if line[1]=='index_swap_read1': #increase the count of index swaps by 1
		index_swaps+=int(line[1])
	if line[1]=='bad_quality_read1': #increase the count of bad_quality records by 1
		bad_quality+=int(line[1])
	number_records.append(int(line[0])/4) #append line count divided by four, since there are four lines per record
	names.append(line[1])
f.close()
distribution(names,number_records) #bar plots the bucket on the x-axis and counts on the y-axis
summ=sum(number_records)#counts the total number of files
f=open('stats', 'w')# open up a file to push some stats to
print("The total number of records read from '1294_S1_L008_R1_001.fastq.gz' is: ", args.number_lines, file=f)
print('The total number of records in buckets: ', summ)
print('The total number of records in the index swapped buckets is: ', index_swaps, file=f)
print('The percent of reads in the index_swap bucket is: ', 100*index_swaps/summ,file=f)
print('The percent of reads in the bad_quality_bucket (w/ cutoff=35) is: ', 100*bad_quality/summ,file=f)
f.close()