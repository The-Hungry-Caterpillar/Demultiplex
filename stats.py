def get_args(): #defines all the independent variables
	import argparse
	parser = argparse.ArgumentParser(description = "still need description")
	#parser.add_argument('- command line variable', '-- python variable', description)
	parser.add_argument('-f', '--input_file', help='filename for input')
	parser.add_argument('-Q', '--qscore', type=int, help='input average qscore cutoff')
	return parser.parse_args()
args=get_args()
x_data=[]
y_data=[]
bad_quality=0
index_swapped=0
f=open(args.input_file,'r')
while True:
	line=f.readline().strip().split(' ') #will look like ["number of lines", "index"]
	if line==['']:
		break
	if (line[1].split('/')[1]).split('_')[0]=='bad-quality':
		bad_quality=int(line[0])/4
	if (line[1].split('/')[1]).split('_')[0]=='index-swap':
		index_swapped=(int(line[0])/4)
	y_data.append(int(line[0])/4)
	x_data.append((line[1].split('/')[1]).split('_')[0])
	#if 'index_swap_read1' in line[1]: #increase the count of index swaps by 1
	#	index_swaps+=int(line[0])
	#if 'bad_quality_read1'in line[1]: #increase the count of bad_quality records by 1
	#	bad_quality+=int(line[0])
	#number_records.append(int(line[0])/4) #append line count divided by four, since there are four lines per record
	#names.append(line[1].split('/')[1]) #this transforms "buckets/index" --> "index"
f.close()

def distribution(x_data,y_data, print_to_terminal = False):
	'''input x_data and y_data and out comes a bargraph! Set True if you want the graph to pop up, otherwise it will just save as a png file'''
	import matplotlib.pyplot as plt
	plt.xlabel('Bucket', size=15)
	plt.ylabel('# fastq records in bucket', size=15)
	plt.xticks(rotation=45,horizontalalignment='right')
	plt.title('Bucket dist, Qcutoff{} (read1)'.format(args.qscore), size = 18)
	plt.bar(x_data,y_data, color='mediumspringgreen',width=1)
	plt.tight_layout()
	plt.savefig('read1_bucket_distribution_Qcut{}.png'.format(args.qscore), dpi=100)
	if print_to_terminal == True:
		plt.show()

distribution(x_data,y_data)
f=open('stats', 'a')
print('\nWith an avg Qscore cutoff of {}, the percent of records in bad_quality bucket is: '.format(args.qscore), round(100*int(bad_quality)/sum(y_data),1), '%', file=f)
print('With an avg Qscore cutoff of {}, the number of records in bad_quality bucket is: '.format(args.qscore), int(bad_quality), file=f)
print('With an avg Qscore cutoff of {}, the percent of records in index swapped bucket is: '.format(args.qscore), round(100*int(index_swapped)/sum(y_data),1), '%', file=f)
print('With an avg Qscore cutoff of {}, the number of records in index swapped bucket is: '.format(args.qscore), int(index_swapped), file=f)
f.close()